"""Main entry point for Gousto recipe scraper."""

import asyncio
import argparse
from datetime import datetime
from typing import Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from loguru import logger
from sqlalchemy import select, func

from src.config import settings
from src.database import init_db, get_session, get_engine, get_session_factory
from src.database.models import (
    Recipe, Nutrition, Ingredient, CookingStep,
    Category, Equipment, Allergen,
)
from src.scrapers import GoustoScraper, RecipeParser
from src.exporters import JSONExporter, CSVExporter
from src.utils import setup_logging

console = Console()


async def save_recipe(session, recipe_data, parser_result):
    """Save parsed recipe to database."""
    from src.models.recipe import RecipeModel

    # Check if recipe already exists
    existing = await session.execute(
        select(Recipe).where(Recipe.url == recipe_data.url)
    )
    if existing.scalar_one_or_none():
        logger.debug(f"Recipe already exists: {recipe_data.title}")
        return None

    # Create main recipe
    recipe = Recipe(
        gousto_id=recipe_data.gousto_id,
        url=recipe_data.url,
        title=recipe_data.title,
        slug=recipe_data.slug,
        description=recipe_data.description,
        image_url=recipe_data.image_url,
        prep_time_minutes=recipe_data.prep_time_minutes,
        cook_time_minutes=recipe_data.cook_time_minutes,
        total_time_minutes=recipe_data.total_time_minutes or recipe_data.calculate_total_time(),
        cuisine=recipe_data.cuisine,
        diet_type=recipe_data.diet_type,
        difficulty=recipe_data.difficulty,
        servings=recipe_data.servings,
        rating=recipe_data.rating,
        rating_count=recipe_data.rating_count,
        scraped_at=datetime.utcnow(),
    )

    # Add nutrition
    if recipe_data.nutrition:
        n = recipe_data.nutrition
        recipe.nutrition = Nutrition(
            calories_kcal=n.calories_kcal,
            protein_grams=n.protein_grams,
            fat_grams=n.fat_grams,
            saturated_fat_grams=n.saturated_fat_grams,
            carbs_grams=n.carbs_grams,
            sugar_grams=n.sugar_grams,
            fibre_grams=n.fibre_grams,
            salt_grams=n.salt_grams,
        )

    # Add ingredients
    for ing in recipe_data.ingredients:
        recipe.ingredients.append(Ingredient(
            name=ing.name,
            quantity=ing.quantity,
            unit=ing.unit,
            raw_text=ing.raw_text,
            preparation_note=ing.preparation_note,
            is_optional=ing.is_optional,
            display_order=ing.display_order,
        ))

    # Add cooking steps
    for step in recipe_data.cooking_steps:
        recipe.cooking_steps.append(CookingStep(
            step_number=step.step_number,
            instruction=step.instruction,
            duration_minutes=step.duration_minutes,
            tip=step.tip,
            image_url=step.image_url,
        ))

    # Add categories
    for cat_name in recipe_data.categories:
        if cat_name:
            # Get or create category
            result = await session.execute(
                select(Category).where(Category.name == cat_name)
            )
            category = result.scalar_one_or_none()
            if not category:
                category = Category(
                    name=cat_name,
                    slug=cat_name.lower().replace(" ", "-"),
                )
                session.add(category)
            recipe.categories.append(category)

    # Add equipment
    for eq_name in recipe_data.equipment:
        if eq_name:
            result = await session.execute(
                select(Equipment).where(Equipment.name == eq_name)
            )
            equipment = result.scalar_one_or_none()
            if not equipment:
                equipment = Equipment(name=eq_name)
                session.add(equipment)
            recipe.equipment_items.append(equipment)

    # Add allergens
    for al_name in recipe_data.allergens:
        if al_name:
            result = await session.execute(
                select(Allergen).where(Allergen.name == al_name)
            )
            allergen = result.scalar_one_or_none()
            if not allergen:
                allergen = Allergen(name=al_name)
                session.add(allergen)
            recipe.allergen_items.append(allergen)

    session.add(recipe)
    return recipe


async def scrape_recipes(max_recipes: Optional[int] = None, skip_existing: bool = True):
    """Main scraping function."""
    setup_logging()

    console.print("[bold blue]Gousto Recipe Scraper[/bold blue]")
    console.print(f"Database: {settings.database_url}")
    console.print()

    # Initialize database
    engine = get_engine()
    await init_db(engine)
    session_factory = get_session_factory(engine)

    parser = RecipeParser()
    scraped_count = 0
    error_count = 0

    async with GoustoScraper() as scraper:
        # Discover recipe URLs
        with console.status("[bold green]Discovering recipes..."):
            recipe_urls = await scraper.discover_recipe_urls(max_recipes=max_recipes)

        console.print(f"[green]Found {len(recipe_urls)} recipes[/green]")

        # Scrape each recipe
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Scraping recipes...", total=len(recipe_urls))

            for url in recipe_urls:
                try:
                    async with session_factory() as session:
                        # Check if already scraped
                        if skip_existing:
                            result = await session.execute(
                                select(Recipe).where(Recipe.url == url)
                            )
                            if result.scalar_one_or_none():
                                logger.debug(f"Skipping existing: {url}")
                                progress.update(task, advance=1)
                                continue

                        # Fetch and parse
                        html = await scraper.fetch_recipe_html(url)
                        recipe_data = parser.parse(html, url)

                        # Save to database
                        saved_recipe = await save_recipe(session, recipe_data, parser)
                        if saved_recipe:
                            await session.commit()
                            scraped_count += 1
                            logger.info(f"Saved: {recipe_data.title}")

                except Exception as e:
                    error_count += 1
                    logger.error(f"Error scraping {url}: {e}")

                progress.update(task, advance=1)

    # Print summary
    console.print()
    table = Table(title="Scraping Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Total URLs", str(len(recipe_urls)))
    table.add_row("Recipes Scraped", str(scraped_count))
    table.add_row("Errors", str(error_count))
    console.print(table)


async def export_data(format: str = "both"):
    """Export scraped data."""
    setup_logging()

    console.print("[bold blue]Exporting Recipe Data[/bold blue]")

    engine = get_engine()
    session_factory = get_session_factory(engine)

    async with session_factory() as session:
        # Count recipes
        result = await session.execute(select(func.count(Recipe.id)))
        count = result.scalar()
        console.print(f"Found {count} recipes to export")

        if count == 0:
            console.print("[yellow]No recipes to export. Run scraper first.[/yellow]")
            return

        if format in ("json", "both"):
            exporter = JSONExporter()
            json_path = await exporter.export_all(session)
            console.print(f"[green]JSON exported to: {json_path}[/green]")

        if format in ("csv", "both"):
            exporter = CSVExporter()
            csv_paths = await exporter.export_all(session)
            for name, path in csv_paths.items():
                console.print(f"[green]CSV ({name}) exported to: {path}[/green]")


async def show_stats():
    """Show database statistics."""
    setup_logging()

    engine = get_engine()
    session_factory = get_session_factory(engine)

    async with session_factory() as session:
        # Get counts
        recipe_count = (await session.execute(select(func.count(Recipe.id)))).scalar()
        ingredient_count = (await session.execute(select(func.count(Ingredient.id)))).scalar()
        step_count = (await session.execute(select(func.count(CookingStep.id)))).scalar()
        category_count = (await session.execute(select(func.count(Category.id)))).scalar()

        table = Table(title="Database Statistics")
        table.add_column("Table", style="cyan")
        table.add_column("Count", style="green")
        table.add_row("Recipes", str(recipe_count))
        table.add_row("Ingredients", str(ingredient_count))
        table.add_row("Cooking Steps", str(step_count))
        table.add_row("Categories", str(category_count))
        console.print(table)

        # Show cuisine breakdown
        if recipe_count > 0:
            result = await session.execute(
                select(Recipe.cuisine, func.count(Recipe.id))
                .where(Recipe.cuisine.isnot(None))
                .group_by(Recipe.cuisine)
                .order_by(func.count(Recipe.id).desc())
                .limit(10)
            )

            cuisine_table = Table(title="Top Cuisines")
            cuisine_table.add_column("Cuisine", style="cyan")
            cuisine_table.add_column("Recipes", style="green")
            for cuisine, count in result:
                cuisine_table.add_row(cuisine, str(count))
            console.print(cuisine_table)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Gousto Recipe Scraper")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Scrape command
    scrape_parser = subparsers.add_parser("scrape", help="Scrape recipes")
    scrape_parser.add_argument(
        "--max", "-m", type=int, default=None,
        help="Maximum number of recipes to scrape"
    )
    scrape_parser.add_argument(
        "--force", "-f", action="store_true",
        help="Re-scrape existing recipes"
    )

    # Export command
    export_parser = subparsers.add_parser("export", help="Export data")
    export_parser.add_argument(
        "--format", "-f", choices=["json", "csv", "both"],
        default="both", help="Export format"
    )

    # Stats command
    subparsers.add_parser("stats", help="Show database statistics")

    args = parser.parse_args()

    if args.command == "scrape":
        asyncio.run(scrape_recipes(
            max_recipes=args.max,
            skip_existing=not args.force,
        ))
    elif args.command == "export":
        asyncio.run(export_data(format=args.format))
    elif args.command == "stats":
        asyncio.run(show_stats())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
