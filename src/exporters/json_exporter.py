"""JSON export functionality."""

import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from loguru import logger

from src.config import settings
from src.database.models import Recipe


class DecimalEncoder(json.JSONEncoder):
    """JSON encoder that handles Decimal types."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class JSONExporter:
    """Export recipes to JSON format."""

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or settings.export_dir

    async def export_all(self, session: AsyncSession, filename: str = None) -> Path:
        """
        Export all recipes to a JSON file.

        Args:
            session: Database session
            filename: Output filename (default: recipes_YYYYMMDD.json)

        Returns:
            Path to exported file
        """
        if filename is None:
            filename = f"recipes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        output_path = self.output_dir / filename

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
            .order_by(Recipe.title)
        )

        result = await session.execute(stmt)
        recipes = result.scalars().all()

        # Convert to dict
        data = {
            "export_date": datetime.now().isoformat(),
            "total_recipes": len(recipes),
            "recipes": [self._recipe_to_dict(r) for r in recipes],
        }

        # Write to file
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, cls=DecimalEncoder, indent=2, ensure_ascii=False)

        logger.info(f"Exported {len(recipes)} recipes to {output_path}")
        return output_path

    async def export_recipe(self, session: AsyncSession, recipe_id: int) -> dict:
        """Export a single recipe as dict."""
        stmt = (
            select(Recipe)
            .where(Recipe.id == recipe_id)
            .options(
                selectinload(Recipe.nutrition),
                selectinload(Recipe.ingredients),
                selectinload(Recipe.cooking_steps),
                selectinload(Recipe.categories),
                selectinload(Recipe.equipment_items),
                selectinload(Recipe.allergen_items),
            )
        )

        result = await session.execute(stmt)
        recipe = result.scalar_one_or_none()

        if recipe:
            return self._recipe_to_dict(recipe)
        return {}

    def _recipe_to_dict(self, recipe: Recipe) -> dict:
        """Convert Recipe model to dict."""
        return {
            "id": recipe.id,
            "gousto_id": recipe.gousto_id,
            "url": recipe.url,
            "title": recipe.title,
            "slug": recipe.slug,
            "description": recipe.description,
            "image_url": recipe.image_url,
            "timing": {
                "prep_minutes": recipe.prep_time_minutes,
                "cook_minutes": recipe.cook_time_minutes,
                "total_minutes": recipe.total_time_minutes,
            },
            "classification": {
                "cuisine": recipe.cuisine,
                "diet_type": recipe.diet_type,
                "meal_type": recipe.meal_type,
                "difficulty": recipe.difficulty,
            },
            "servings": recipe.servings,
            "rating": {
                "value": float(recipe.rating) if recipe.rating else None,
                "count": recipe.rating_count,
            },
            "nutrition": self._nutrition_to_dict(recipe.nutrition) if recipe.nutrition else None,
            "ingredients": [
                {
                    "name": ing.name,
                    "quantity": ing.quantity,
                    "unit": ing.unit,
                    "raw_text": ing.raw_text,
                    "preparation_note": ing.preparation_note,
                    "is_optional": ing.is_optional,
                }
                for ing in recipe.ingredients
            ],
            "cooking_steps": [
                {
                    "step_number": step.step_number,
                    "instruction": step.instruction,
                    "duration_minutes": step.duration_minutes,
                    "tip": step.tip,
                    "image_url": step.image_url,
                }
                for step in recipe.cooking_steps
            ],
            "categories": [cat.name for cat in recipe.categories],
            "equipment": [eq.name for eq in recipe.equipment_items],
            "allergens": [al.name for al in recipe.allergen_items],
            "scraped_at": recipe.scraped_at.isoformat() if recipe.scraped_at else None,
        }

    def _nutrition_to_dict(self, nutrition) -> dict:
        """Convert Nutrition model to dict."""
        return {
            "calories_kcal": nutrition.calories_kcal,
            "protein_grams": float(nutrition.protein_grams) if nutrition.protein_grams else None,
            "fat_grams": float(nutrition.fat_grams) if nutrition.fat_grams else None,
            "saturated_fat_grams": float(nutrition.saturated_fat_grams) if nutrition.saturated_fat_grams else None,
            "carbs_grams": float(nutrition.carbs_grams) if nutrition.carbs_grams else None,
            "sugar_grams": float(nutrition.sugar_grams) if nutrition.sugar_grams else None,
            "fibre_grams": float(nutrition.fibre_grams) if nutrition.fibre_grams else None,
            "salt_grams": float(nutrition.salt_grams) if nutrition.salt_grams else None,
        }
