"""Main Gousto recipe scraper using Playwright."""

import asyncio
import re
from typing import Optional
from urllib.parse import urljoin

from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeout
from loguru import logger

from src.config import settings
from src.utils.rate_limiter import AdaptiveRateLimiter
from src.utils.retry import with_retry


class GoustoScraper:
    """Scraper for discovering and fetching Gousto recipes."""

    def __init__(self):
        self.base_url = settings.base_url
        self.cookbook_url = settings.cookbook_url
        self.rate_limiter = AdaptiveRateLimiter(
            initial_delay=settings.request_delay_seconds,
            min_delay=2.0,
            max_delay=15.0,
        )
        self.browser: Optional[Browser] = None
        self._playwright = None

    async def __aenter__(self):
        """Start browser on context entry."""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close browser on context exit."""
        await self.close()

    async def start(self) -> None:
        """Start the Playwright browser."""
        logger.info("Starting Playwright browser...")
        self._playwright = await async_playwright().start()
        self.browser = await self._playwright.chromium.launch(
            headless=settings.headless,
            slow_mo=settings.slow_mo,
        )
        logger.info("Browser started successfully")

    async def close(self) -> None:
        """Close the browser and cleanup."""
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
        logger.info("Browser closed")

    async def _create_page(self) -> Page:
        """Create a new browser page with settings."""
        if not self.browser:
            raise RuntimeError("Browser not started. Call start() first.")

        context = await self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        page = await context.new_page()

        # Block unnecessary resources for faster loading
        await page.route(
            "**/*.{png,jpg,jpeg,gif,svg,webp,woff,woff2,ttf,eot}",
            lambda route: route.abort(),
        )

        return page

    @with_retry(max_attempts=3, initial_delay=2.0)
    async def discover_recipe_urls(self, max_recipes: Optional[int] = None) -> list[str]:
        """
        Discover all recipe URLs from the cookbook listing page.

        Args:
            max_recipes: Maximum number of recipes to discover (None for all)

        Returns:
            List of recipe URLs
        """
        logger.info(f"Discovering recipe URLs from {self.cookbook_url}")
        page = await self._create_page()

        try:
            await page.goto(self.cookbook_url, wait_until="networkidle", timeout=60000)

            # Wait for recipe cards to load
            await page.wait_for_selector(
                'a[href*="/cookbook/"]',
                timeout=30000,
            )

            all_urls = set()
            scroll_attempts = 0
            max_scroll_attempts = 100  # Safety limit

            while scroll_attempts < max_scroll_attempts:
                # Extract current recipe URLs
                urls = await page.evaluate('''
                    () => {
                        const links = document.querySelectorAll('a[href*="/cookbook/"]');
                        return Array.from(links)
                            .map(a => a.href)
                            .filter(href => {
                                // Filter for individual recipe pages
                                const parts = href.split('/');
                                // URLs like /cookbook/chicken-recipes/some-recipe-name
                                return parts.length >= 5 &&
                                       href.includes('-recipes/') &&
                                       !href.endsWith('/recipes') &&
                                       !href.includes('?');
                            });
                    }
                ''')

                new_urls = set(urls) - all_urls
                if new_urls:
                    logger.debug(f"Found {len(new_urls)} new recipes (total: {len(all_urls) + len(new_urls)})")
                    all_urls.update(new_urls)

                # Check if we have enough
                if max_recipes and len(all_urls) >= max_recipes:
                    logger.info(f"Reached max recipes limit: {max_recipes}")
                    break

                # Try to load more recipes
                previous_count = len(all_urls)

                # Look for "Load More" or "See More" button
                load_more_selectors = [
                    'button:has-text("Load more")',
                    'button:has-text("See more")',
                    'button:has-text("Show more")',
                    '[data-testid="load-more"]',
                    '.load-more-button',
                ]

                button_clicked = False
                for selector in load_more_selectors:
                    try:
                        button = page.locator(selector).first
                        if await button.is_visible(timeout=1000):
                            await button.click()
                            await asyncio.sleep(2)
                            button_clicked = True
                            break
                    except Exception:
                        continue

                # If no button, try scrolling
                if not button_clicked:
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await asyncio.sleep(2)

                # Check if we got new recipes
                urls_after = await page.evaluate('''
                    () => {
                        const links = document.querySelectorAll('a[href*="/cookbook/"]');
                        return Array.from(links)
                            .map(a => a.href)
                            .filter(href => href.includes('-recipes/') && !href.endsWith('/recipes'));
                    }
                ''')
                all_urls.update(urls_after)

                if len(all_urls) == previous_count:
                    scroll_attempts += 1
                    if scroll_attempts >= 3:
                        logger.info("No new recipes found after 3 attempts, stopping")
                        break
                else:
                    scroll_attempts = 0

            recipe_urls = sorted(list(all_urls))
            if max_recipes:
                recipe_urls = recipe_urls[:max_recipes]

            logger.info(f"Discovered {len(recipe_urls)} recipe URLs")
            return recipe_urls

        except PlaywrightTimeout as e:
            logger.error(f"Timeout discovering recipes: {e}")
            raise
        finally:
            await page.context.close()

    @with_retry(max_attempts=3, initial_delay=2.0)
    async def fetch_recipe_html(self, url: str) -> str:
        """
        Fetch the HTML content of a recipe page.

        Args:
            url: Recipe URL to fetch

        Returns:
            HTML content of the page
        """
        await self.rate_limiter.acquire()

        logger.debug(f"Fetching recipe: {url}")
        page = await self._create_page()

        try:
            response = await page.goto(url, wait_until="networkidle", timeout=30000)

            if response and response.status >= 400:
                self.rate_limiter.record_failure(is_rate_limit=response.status == 429)
                raise Exception(f"HTTP {response.status} for {url}")

            # Wait for recipe content to load
            try:
                await page.wait_for_selector(
                    'h1, [data-testid="recipe-title"], .recipe-title',
                    timeout=10000,
                )
            except PlaywrightTimeout:
                logger.warning(f"Recipe title not found on {url}, proceeding anyway")

            # Wait a bit more for dynamic content
            await asyncio.sleep(1)

            html = await page.content()
            self.rate_limiter.record_success()

            logger.debug(f"Successfully fetched {url} ({len(html)} bytes)")
            return html

        except Exception as e:
            self.rate_limiter.record_failure()
            logger.error(f"Error fetching {url}: {e}")
            raise
        finally:
            await page.context.close()

    async def discover_category_urls(self) -> list[dict]:
        """
        Discover recipe category pages for more comprehensive scraping.

        Returns:
            List of category info dicts with name and url
        """
        logger.info("Discovering category URLs...")
        page = await self._create_page()

        try:
            await page.goto(self.cookbook_url, wait_until="networkidle", timeout=60000)

            categories = await page.evaluate('''
                () => {
                    const links = document.querySelectorAll('a[href*="/cookbook/"]');
                    const categories = [];
                    const seen = new Set();

                    links.forEach(link => {
                        const href = link.href;
                        // Match category pages like /cookbook/chicken-recipes
                        if (href.match(/\\/cookbook\\/[a-z-]+-recipes\\/?$/) && !seen.has(href)) {
                            seen.add(href);
                            categories.push({
                                name: link.textContent?.trim() || href.split('/').pop(),
                                url: href
                            });
                        }
                    });

                    return categories;
                }
            ''')

            logger.info(f"Found {len(categories)} categories")
            return categories

        finally:
            await page.context.close()
