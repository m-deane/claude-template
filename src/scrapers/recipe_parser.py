"""Recipe parser for extracting data from Gousto recipe pages."""

import json
import re
from decimal import Decimal
from typing import Any, Optional

from bs4 import BeautifulSoup
from loguru import logger

from src.models.recipe import (
    RecipeModel,
    IngredientModel,
    CookingStepModel,
    NutritionModel,
)


class RecipeParser:
    """Parser for extracting recipe data from HTML."""

    def __init__(self):
        self._recipe_scrapers_available = False
        try:
            from recipe_scrapers import scrape_html
            self._scrape_html = scrape_html
            self._recipe_scrapers_available = True
        except ImportError:
            logger.warning("recipe-scrapers not available, using fallback parser")

    def parse(self, html: str, url: str) -> RecipeModel:
        """
        Parse recipe data from HTML content.

        Args:
            html: Raw HTML content
            url: Original recipe URL

        Returns:
            Validated RecipeModel
        """
        soup = BeautifulSoup(html, "lxml")

        # Try recipe-scrapers library first
        if self._recipe_scrapers_available:
            try:
                return self._parse_with_library(html, url, soup)
            except Exception as e:
                logger.warning(f"recipe-scrapers failed, using fallback: {e}")

        # Fallback to custom parsing
        return self._parse_fallback(soup, url)

    def _parse_with_library(self, html: str, url: str, soup: BeautifulSoup) -> RecipeModel:
        """Parse using recipe-scrapers library."""
        scraper = self._scrape_html(html, url)

        # Extract basic info
        title = scraper.title() or self._extract_title(soup)
        description = self._extract_description(soup)
        image_url = scraper.image()

        # Extract times
        total_time = scraper.total_time()
        prep_time = scraper.prep_time()
        cook_time = scraper.cook_time()

        # Extract ingredients
        raw_ingredients = scraper.ingredients() or []
        ingredients = [
            IngredientModel.from_raw_text(ing, i)
            for i, ing in enumerate(raw_ingredients)
        ]

        # Extract instructions
        instructions_text = scraper.instructions() or ""
        cooking_steps = self._parse_instructions(instructions_text)

        # Extract nutrition
        nutrients = scraper.nutrients() or {}
        nutrition = NutritionModel.from_dict(nutrients) if nutrients else None

        # Extract servings
        yields = scraper.yields() or "2"
        servings = self._parse_servings(yields)

        # Extract additional data from soup
        cuisine = self._extract_cuisine(soup)
        diet_type = self._extract_diet_type(soup)
        difficulty = self._extract_difficulty(soup)
        rating, rating_count = self._extract_rating(soup)
        categories = self._extract_categories(soup)
        equipment = self._extract_equipment(soup)
        allergens = self._extract_allergens(soup)

        # Try to get gousto_id from URL or page
        gousto_id = self._extract_gousto_id(url, soup)

        return RecipeModel(
            url=url,
            gousto_id=gousto_id,
            title=title,
            description=description,
            image_url=image_url,
            prep_time_minutes=prep_time,
            cook_time_minutes=cook_time,
            total_time_minutes=total_time,
            cuisine=cuisine,
            diet_type=diet_type,
            difficulty=difficulty,
            servings=servings,
            rating=Decimal(str(rating)) if rating else None,
            rating_count=rating_count,
            ingredients=ingredients,
            cooking_steps=cooking_steps,
            nutrition=nutrition,
            categories=categories,
            equipment=equipment,
            allergens=allergens,
        )

    def _parse_fallback(self, soup: BeautifulSoup, url: str) -> RecipeModel:
        """Fallback parser when recipe-scrapers is unavailable."""
        # Try to extract JSON-LD data first
        json_ld = self._extract_json_ld(soup)
        if json_ld:
            return self._parse_json_ld(json_ld, url, soup)

        # Manual extraction
        title = self._extract_title(soup)
        description = self._extract_description(soup)
        image_url = self._extract_image(soup)

        # Extract ingredients
        ingredients = self._extract_ingredients_fallback(soup)

        # Extract instructions
        instructions = self._extract_instructions_fallback(soup)
        cooking_steps = self._parse_instructions("\n".join(instructions))

        # Extract times
        prep_time, cook_time, total_time = self._extract_times(soup)

        # Extract nutrition
        nutrition = self._extract_nutrition_fallback(soup)

        return RecipeModel(
            url=url,
            gousto_id=self._extract_gousto_id(url, soup),
            title=title,
            description=description,
            image_url=image_url,
            prep_time_minutes=prep_time,
            cook_time_minutes=cook_time,
            total_time_minutes=total_time,
            cuisine=self._extract_cuisine(soup),
            diet_type=self._extract_diet_type(soup),
            difficulty=self._extract_difficulty(soup),
            servings=self._parse_servings(self._extract_servings(soup)),
            rating=None,
            rating_count=None,
            ingredients=ingredients,
            cooking_steps=cooking_steps,
            nutrition=nutrition,
            categories=self._extract_categories(soup),
            equipment=self._extract_equipment(soup),
            allergens=self._extract_allergens(soup),
        )

    def _extract_json_ld(self, soup: BeautifulSoup) -> Optional[dict]:
        """Extract JSON-LD structured data."""
        scripts = soup.find_all("script", type="application/ld+json")
        for script in scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    for item in data:
                        if item.get("@type") == "Recipe":
                            return item
                elif data.get("@type") == "Recipe":
                    return data
            except (json.JSONDecodeError, AttributeError):
                continue
        return None

    def _parse_json_ld(self, data: dict, url: str, soup: BeautifulSoup) -> RecipeModel:
        """Parse recipe from JSON-LD data."""
        # Parse ingredients
        raw_ingredients = data.get("recipeIngredient", [])
        ingredients = [
            IngredientModel.from_raw_text(ing, i)
            for i, ing in enumerate(raw_ingredients)
        ]

        # Parse instructions
        raw_instructions = data.get("recipeInstructions", [])
        cooking_steps = []
        for i, step in enumerate(raw_instructions):
            if isinstance(step, str):
                cooking_steps.append(CookingStepModel(
                    step_number=i + 1,
                    instruction=step,
                ))
            elif isinstance(step, dict):
                cooking_steps.append(CookingStepModel(
                    step_number=i + 1,
                    instruction=step.get("text", ""),
                    image_url=step.get("image"),
                ))

        # Parse nutrition
        nutrition_data = data.get("nutrition", {})
        nutrition = NutritionModel.from_dict(nutrition_data) if nutrition_data else None

        # Parse times
        prep_time = self._parse_iso_duration(data.get("prepTime"))
        cook_time = self._parse_iso_duration(data.get("cookTime"))
        total_time = self._parse_iso_duration(data.get("totalTime"))

        # Parse rating
        rating_data = data.get("aggregateRating", {})
        rating = rating_data.get("ratingValue")
        rating_count = rating_data.get("ratingCount")

        return RecipeModel(
            url=url,
            gousto_id=self._extract_gousto_id(url, soup),
            title=data.get("name", ""),
            description=data.get("description"),
            image_url=data.get("image", [None])[0] if isinstance(data.get("image"), list) else data.get("image"),
            prep_time_minutes=prep_time,
            cook_time_minutes=cook_time,
            total_time_minutes=total_time,
            cuisine=data.get("recipeCuisine"),
            diet_type=self._extract_diet_type(soup),
            difficulty=self._extract_difficulty(soup),
            servings=self._parse_servings(data.get("recipeYield", "2")),
            rating=Decimal(str(rating)) if rating else None,
            rating_count=int(rating_count) if rating_count else None,
            ingredients=ingredients,
            cooking_steps=cooking_steps,
            nutrition=nutrition,
            categories=data.get("recipeCategory", []) if isinstance(data.get("recipeCategory"), list) else [data.get("recipeCategory")] if data.get("recipeCategory") else [],
            equipment=self._extract_equipment(soup),
            allergens=self._extract_allergens(soup),
        )

    def _parse_iso_duration(self, duration: Optional[str]) -> Optional[int]:
        """Parse ISO 8601 duration to minutes."""
        if not duration:
            return None

        # Match PT30M, PT1H30M, etc.
        match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?", duration)
        if match:
            hours = int(match.group(1) or 0)
            minutes = int(match.group(2) or 0)
            return hours * 60 + minutes

        return None

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract recipe title."""
        selectors = [
            "h1",
            '[data-testid="recipe-title"]',
            ".recipe-title",
            ".indivrecipe-title",
            'meta[property="og:title"]',
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == "meta":
                    return element.get("content", "").strip()
                return element.get_text(strip=True)

        return "Unknown Recipe"

    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract recipe description."""
        selectors = [
            '[data-testid="recipe-description"]',
            ".recipe-description",
            'meta[property="og:description"]',
            'meta[name="description"]',
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == "meta":
                    return element.get("content", "").strip()
                return element.get_text(strip=True)

        return None

    def _extract_image(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract main recipe image URL."""
        selectors = [
            'meta[property="og:image"]',
            '[data-testid="recipe-image"] img',
            ".recipe-image img",
            ".hero-image img",
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == "meta":
                    return element.get("content")
                return element.get("src")

        return None

    def _extract_ingredients_fallback(self, soup: BeautifulSoup) -> list[IngredientModel]:
        """Extract ingredients using fallback selectors."""
        selectors = [
            ".indivrecipe-ingredients-text",
            '[data-testid="ingredient"]',
            ".recipe-ingredients li",
            ".ingredient-list li",
        ]

        ingredients = []
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                for i, el in enumerate(elements):
                    text = el.get_text(strip=True)
                    if text:
                        ingredients.append(IngredientModel.from_raw_text(text, i))
                break

        return ingredients

    def _extract_instructions_fallback(self, soup: BeautifulSoup) -> list[str]:
        """Extract cooking instructions using fallback selectors."""
        selectors = [
            '[data-testid="instruction"]',
            ".recipe-instructions li",
            ".cooking-steps li",
            ".method-step",
        ]

        instructions = []
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                for el in elements:
                    text = el.get_text(strip=True)
                    if text:
                        instructions.append(text)
                break

        return instructions

    def _parse_instructions(self, text: str) -> list[CookingStepModel]:
        """Parse instruction text into cooking steps."""
        if not text:
            return []

        # Split by common separators
        steps = re.split(r'\n+|\d+\.\s+', text)
        steps = [s.strip() for s in steps if s.strip()]

        return [
            CookingStepModel(
                step_number=i + 1,
                instruction=step,
            )
            for i, step in enumerate(steps)
        ]

    def _extract_times(self, soup: BeautifulSoup) -> tuple[Optional[int], Optional[int], Optional[int]]:
        """Extract prep, cook, and total times."""
        prep_time = None
        cook_time = None
        total_time = None

        time_patterns = [
            (r"prep[:\s]*(\d+)\s*min", "prep"),
            (r"cook[:\s]*(\d+)\s*min", "cook"),
            (r"total[:\s]*(\d+)\s*min", "total"),
            (r"(\d+)\s*min(?:ute)?s?\s*prep", "prep"),
            (r"(\d+)\s*min(?:ute)?s?\s*cook", "cook"),
        ]

        text = soup.get_text()
        for pattern, time_type in time_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = int(match.group(1))
                if time_type == "prep":
                    prep_time = value
                elif time_type == "cook":
                    cook_time = value
                elif time_type == "total":
                    total_time = value

        return prep_time, cook_time, total_time

    def _extract_nutrition_fallback(self, soup: BeautifulSoup) -> Optional[NutritionModel]:
        """Extract nutrition info using fallback parsing."""
        nutrition_data = {}

        # Look for nutrition section
        nutrition_selectors = [
            ".nutrition-info",
            '[data-testid="nutrition"]',
            ".nutritional-info",
        ]

        for selector in nutrition_selectors:
            section = soup.select_one(selector)
            if section:
                text = section.get_text()

                patterns = [
                    (r"(\d+)\s*kcal", "calories_kcal"),
                    (r"protein[:\s]*(\d+(?:\.\d+)?)\s*g", "protein_grams"),
                    (r"fat[:\s]*(\d+(?:\.\d+)?)\s*g", "fat_grams"),
                    (r"carb(?:ohydrate)?s?[:\s]*(\d+(?:\.\d+)?)\s*g", "carbs_grams"),
                    (r"sugar[:\s]*(\d+(?:\.\d+)?)\s*g", "sugar_grams"),
                    (r"fibre?[:\s]*(\d+(?:\.\d+)?)\s*g", "fibre_grams"),
                    (r"salt[:\s]*(\d+(?:\.\d+)?)\s*g", "salt_grams"),
                ]

                for pattern, key in patterns:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        nutrition_data[key] = match.group(1)

                break

        return NutritionModel.from_dict(nutrition_data) if nutrition_data else None

    def _extract_servings(self, soup: BeautifulSoup) -> str:
        """Extract serving size."""
        selectors = [
            '[data-testid="servings"]',
            ".servings",
            ".recipe-yield",
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)

        return "2"

    def _parse_servings(self, text: Any) -> int:
        """Parse servings from text."""
        if isinstance(text, int):
            return text

        text = str(text)
        match = re.search(r"(\d+)", text)
        if match:
            return int(match.group(1))
        return 2

    def _extract_cuisine(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract cuisine type from URL or page."""
        # Try to get from URL path
        for link in soup.find_all("a", href=True):
            href = link.get("href", "")
            match = re.search(r"/cookbook/([a-z]+)-recipes", href)
            if match:
                cuisine = match.group(1)
                if cuisine not in ["all", "quick", "easy", "healthy"]:
                    return cuisine.title()

        return None

    def _extract_diet_type(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract dietary type (vegetarian, vegan, etc.)."""
        text = soup.get_text().lower()

        diet_types = {
            "vegan": "vegan",
            "vegetarian": "vegetarian",
            "pescatarian": "pescatarian",
            "dairy-free": "dairy-free",
            "gluten-free": "gluten-free",
        }

        for keyword, diet in diet_types.items():
            if keyword in text:
                return diet

        return None

    def _extract_difficulty(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract difficulty level."""
        selectors = [
            '[data-testid="difficulty"]',
            ".difficulty",
            ".skill-level",
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)

        return None

    def _extract_rating(self, soup: BeautifulSoup) -> tuple[Optional[float], Optional[int]]:
        """Extract rating and rating count."""
        rating = None
        count = None

        # Look for rating elements
        rating_selectors = [
            '[data-testid="rating"]',
            ".rating",
            ".star-rating",
        ]

        for selector in rating_selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text()
                match = re.search(r"(\d+(?:\.\d+)?)\s*(?:/\s*5)?", text)
                if match:
                    rating = float(match.group(1))

                count_match = re.search(r"\((\d+)\s*(?:review|rating)", text, re.IGNORECASE)
                if count_match:
                    count = int(count_match.group(1))

                break

        return rating, count

    def _extract_categories(self, soup: BeautifulSoup) -> list[str]:
        """Extract recipe categories/tags."""
        categories = []

        tag_selectors = [
            '[data-testid="tag"]',
            ".recipe-tag",
            ".category-tag",
        ]

        for selector in tag_selectors:
            elements = soup.select(selector)
            if elements:
                for el in elements:
                    text = el.get_text(strip=True)
                    if text:
                        categories.append(text)
                break

        return categories

    def _extract_equipment(self, soup: BeautifulSoup) -> list[str]:
        """Extract required equipment."""
        equipment = []

        selectors = [
            '[data-testid="equipment"]',
            ".equipment-item",
            ".kitchen-equipment li",
        ]

        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                for el in elements:
                    text = el.get_text(strip=True)
                    if text:
                        equipment.append(text)
                break

        return equipment

    def _extract_allergens(self, soup: BeautifulSoup) -> list[str]:
        """Extract allergen information."""
        allergens = []

        common_allergens = [
            "gluten", "wheat", "dairy", "milk", "eggs", "nuts",
            "peanuts", "soy", "fish", "shellfish", "sesame", "celery",
            "mustard", "sulphites", "lupin", "molluscs",
        ]

        text = soup.get_text().lower()

        # Look for "contains" statements
        contains_match = re.search(r"contains?[:\s]+([^.]+)", text)
        if contains_match:
            allergen_text = contains_match.group(1)
            for allergen in common_allergens:
                if allergen in allergen_text:
                    allergens.append(allergen.title())

        return allergens

    def _extract_gousto_id(self, url: str, soup: BeautifulSoup) -> Optional[str]:
        """Extract Gousto recipe ID."""
        # Try to get from URL slug
        match = re.search(r"/cookbook/[^/]+/([^/?]+)", url)
        if match:
            return match.group(1)

        return None
