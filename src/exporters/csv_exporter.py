"""CSV export functionality."""

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from loguru import logger

from src.config import settings
from src.database.models import Recipe


class CSVExporter:
    """Export recipes to CSV format."""

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or settings.export_dir

    async def export_all(self, session: AsyncSession, prefix: str = "recipes") -> dict[str, Path]:
        """
        Export all recipes to CSV files.

        Creates multiple CSV files:
        - recipes.csv: Main recipe data
        - ingredients.csv: All ingredients
        - cooking_steps.csv: All cooking instructions
        - nutrition.csv: Nutrition information

        Args:
            session: Database session
            prefix: Filename prefix

        Returns:
            Dict mapping table name to file path
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Fetch all recipes with relationships
        stmt = (
            select(Recipe)
            .options(
                selectinload(Recipe.nutrition),
                selectinload(Recipe.ingredients),
                selectinload(Recipe.cooking_steps),
                selectinload(Recipe.categories),
                selectinload(Recipe.equipment_items),
                selectinload(Recipe.allergen_items),
            )
            .order_by(Recipe.id)
        )

        result = await session.execute(stmt)
        recipes = result.scalars().all()

        exported_files = {}

        # Export main recipes
        recipes_path = self.output_dir / f"{prefix}_{timestamp}.csv"
        self._export_recipes_csv(recipes, recipes_path)
        exported_files["recipes"] = recipes_path

        # Export ingredients
        ingredients_path = self.output_dir / f"{prefix}_ingredients_{timestamp}.csv"
        self._export_ingredients_csv(recipes, ingredients_path)
        exported_files["ingredients"] = ingredients_path

        # Export cooking steps
        steps_path = self.output_dir / f"{prefix}_steps_{timestamp}.csv"
        self._export_steps_csv(recipes, steps_path)
        exported_files["cooking_steps"] = steps_path

        # Export nutrition
        nutrition_path = self.output_dir / f"{prefix}_nutrition_{timestamp}.csv"
        self._export_nutrition_csv(recipes, nutrition_path)
        exported_files["nutrition"] = nutrition_path

        logger.info(f"Exported {len(recipes)} recipes to {len(exported_files)} CSV files")
        return exported_files

    def _export_recipes_csv(self, recipes: list[Recipe], path: Path) -> None:
        """Export main recipe data to CSV."""
        headers = [
            "id", "gousto_id", "url", "title", "slug", "description",
            "image_url", "prep_time_minutes", "cook_time_minutes",
            "total_time_minutes", "cuisine", "diet_type", "meal_type",
            "difficulty", "servings", "rating", "rating_count",
            "categories", "equipment", "allergens", "scraped_at",
        ]

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for recipe in recipes:
                writer.writerow({
                    "id": recipe.id,
                    "gousto_id": recipe.gousto_id,
                    "url": recipe.url,
                    "title": recipe.title,
                    "slug": recipe.slug,
                    "description": recipe.description,
                    "image_url": recipe.image_url,
                    "prep_time_minutes": recipe.prep_time_minutes,
                    "cook_time_minutes": recipe.cook_time_minutes,
                    "total_time_minutes": recipe.total_time_minutes,
                    "cuisine": recipe.cuisine,
                    "diet_type": recipe.diet_type,
                    "meal_type": recipe.meal_type,
                    "difficulty": recipe.difficulty,
                    "servings": recipe.servings,
                    "rating": float(recipe.rating) if recipe.rating else None,
                    "rating_count": recipe.rating_count,
                    "categories": "|".join(cat.name for cat in recipe.categories),
                    "equipment": "|".join(eq.name for eq in recipe.equipment_items),
                    "allergens": "|".join(al.name for al in recipe.allergen_items),
                    "scraped_at": recipe.scraped_at.isoformat() if recipe.scraped_at else None,
                })

        logger.debug(f"Exported recipes to {path}")

    def _export_ingredients_csv(self, recipes: list[Recipe], path: Path) -> None:
        """Export ingredients to CSV."""
        headers = [
            "recipe_id", "recipe_title", "display_order", "name",
            "quantity", "unit", "raw_text", "preparation_note", "is_optional",
        ]

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for recipe in recipes:
                for ing in recipe.ingredients:
                    writer.writerow({
                        "recipe_id": recipe.id,
                        "recipe_title": recipe.title,
                        "display_order": ing.display_order,
                        "name": ing.name,
                        "quantity": ing.quantity,
                        "unit": ing.unit,
                        "raw_text": ing.raw_text,
                        "preparation_note": ing.preparation_note,
                        "is_optional": ing.is_optional,
                    })

        logger.debug(f"Exported ingredients to {path}")

    def _export_steps_csv(self, recipes: list[Recipe], path: Path) -> None:
        """Export cooking steps to CSV."""
        headers = [
            "recipe_id", "recipe_title", "step_number",
            "instruction", "duration_minutes", "tip", "image_url",
        ]

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for recipe in recipes:
                for step in recipe.cooking_steps:
                    writer.writerow({
                        "recipe_id": recipe.id,
                        "recipe_title": recipe.title,
                        "step_number": step.step_number,
                        "instruction": step.instruction,
                        "duration_minutes": step.duration_minutes,
                        "tip": step.tip,
                        "image_url": step.image_url,
                    })

        logger.debug(f"Exported cooking steps to {path}")

    def _export_nutrition_csv(self, recipes: list[Recipe], path: Path) -> None:
        """Export nutrition data to CSV."""
        headers = [
            "recipe_id", "recipe_title", "calories_kcal", "protein_grams",
            "fat_grams", "saturated_fat_grams", "carbs_grams",
            "sugar_grams", "fibre_grams", "salt_grams",
        ]

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()

            for recipe in recipes:
                if recipe.nutrition:
                    n = recipe.nutrition
                    writer.writerow({
                        "recipe_id": recipe.id,
                        "recipe_title": recipe.title,
                        "calories_kcal": n.calories_kcal,
                        "protein_grams": float(n.protein_grams) if n.protein_grams else None,
                        "fat_grams": float(n.fat_grams) if n.fat_grams else None,
                        "saturated_fat_grams": float(n.saturated_fat_grams) if n.saturated_fat_grams else None,
                        "carbs_grams": float(n.carbs_grams) if n.carbs_grams else None,
                        "sugar_grams": float(n.sugar_grams) if n.sugar_grams else None,
                        "fibre_grams": float(n.fibre_grams) if n.fibre_grams else None,
                        "salt_grams": float(n.salt_grams) if n.salt_grams else None,
                    })

        logger.debug(f"Exported nutrition to {path}")
