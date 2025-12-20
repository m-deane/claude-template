"""Pydantic models for recipe data validation."""

import re
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class IngredientModel(BaseModel):
    """Validated ingredient data."""

    name: str
    quantity: Optional[str] = None
    unit: Optional[str] = None
    raw_text: Optional[str] = None
    preparation_note: Optional[str] = None
    is_optional: bool = False
    display_order: int = 0

    @classmethod
    def from_raw_text(cls, text: str, order: int = 0) -> "IngredientModel":
        """Parse ingredient from raw text string."""
        text = text.strip()

        # Common patterns: "2 tbsp olive oil", "1 chicken breast", "Salt to taste"
        quantity_pattern = r"^([\d½¼¾⅓⅔]+(?:\s*[-–]\s*[\d½¼¾⅓⅔]+)?)\s*"
        unit_pattern = r"(tbsp|tsp|g|kg|ml|l|cup|cups|oz|lb|bunch|clove|cloves|pinch|handful|pack|tin|can)s?\s+"

        quantity = None
        unit = None
        name = text

        # Extract quantity
        qty_match = re.match(quantity_pattern, text)
        if qty_match:
            quantity = qty_match.group(1).strip()
            remaining = text[qty_match.end() :].strip()

            # Extract unit
            unit_match = re.match(unit_pattern, remaining, re.IGNORECASE)
            if unit_match:
                unit = unit_match.group(1).lower()
                name = remaining[unit_match.end() :].strip()
            else:
                name = remaining

        # Check for optional
        is_optional = "(optional)" in name.lower()
        name = re.sub(r"\s*\(optional\)\s*", "", name, flags=re.IGNORECASE).strip()

        # Extract preparation notes (e.g., "finely chopped", "diced")
        prep_patterns = [
            r",?\s*(finely\s+)?(chopped|diced|sliced|minced|crushed|grated)",
            r",?\s*(to\s+taste)",
            r",?\s*(at\s+room\s+temperature)",
        ]
        preparation_note = None
        for pattern in prep_patterns:
            prep_match = re.search(pattern, name, re.IGNORECASE)
            if prep_match:
                preparation_note = prep_match.group(0).strip(" ,")
                name = name[: prep_match.start()].strip()
                break

        return cls(
            name=name or text,
            quantity=quantity,
            unit=unit,
            raw_text=text,
            preparation_note=preparation_note,
            is_optional=is_optional,
            display_order=order,
        )


class CookingStepModel(BaseModel):
    """Validated cooking step data."""

    step_number: int
    instruction: str
    duration_minutes: Optional[int] = None
    tip: Optional[str] = None
    image_url: Optional[str] = None

    @field_validator("instruction")
    @classmethod
    def clean_instruction(cls, v: str) -> str:
        """Clean up instruction text."""
        # Remove extra whitespace
        v = re.sub(r"\s+", " ", v).strip()
        return v


class NutritionModel(BaseModel):
    """Validated nutrition data per serving."""

    calories_kcal: Optional[int] = None
    protein_grams: Optional[Decimal] = None
    fat_grams: Optional[Decimal] = None
    saturated_fat_grams: Optional[Decimal] = None
    carbs_grams: Optional[Decimal] = None
    sugar_grams: Optional[Decimal] = None
    fibre_grams: Optional[Decimal] = None
    salt_grams: Optional[Decimal] = None

    @classmethod
    def from_dict(cls, data: dict) -> "NutritionModel":
        """Parse nutrition from various dict formats."""
        # Handle different key formats
        mapping = {
            "calories": "calories_kcal",
            "caloriesKcal": "calories_kcal",
            "calories_kcal": "calories_kcal",
            "energy": "calories_kcal",
            "protein": "protein_grams",
            "proteinGrams": "protein_grams",
            "protein_grams": "protein_grams",
            "fat": "fat_grams",
            "fatGrams": "fat_grams",
            "fat_grams": "fat_grams",
            "saturatedFat": "saturated_fat_grams",
            "saturated_fat_grams": "saturated_fat_grams",
            "carbs": "carbs_grams",
            "carbsGrams": "carbs_grams",
            "carbs_grams": "carbs_grams",
            "carbohydrates": "carbs_grams",
            "sugar": "sugar_grams",
            "sugarGrams": "sugar_grams",
            "sugar_grams": "sugar_grams",
            "fibre": "fibre_grams",
            "fiber": "fibre_grams",
            "fibreGrams": "fibre_grams",
            "fibre_grams": "fibre_grams",
            "salt": "salt_grams",
            "saltGrams": "salt_grams",
            "salt_grams": "salt_grams",
        }

        parsed = {}
        for key, value in data.items():
            normalized_key = mapping.get(key.lower().replace("-", "_").replace(" ", "_"))
            if normalized_key and value is not None:
                # Extract numeric value
                if isinstance(value, str):
                    match = re.search(r"[\d.]+", value)
                    if match:
                        try:
                            num_val = float(match.group())
                            if normalized_key == "calories_kcal":
                                parsed[normalized_key] = int(num_val)
                            else:
                                parsed[normalized_key] = Decimal(str(num_val))
                        except (ValueError, TypeError):
                            pass
                elif isinstance(value, (int, float)):
                    if normalized_key == "calories_kcal":
                        parsed[normalized_key] = int(value)
                    else:
                        parsed[normalized_key] = Decimal(str(value))

        return cls(**parsed)


class RecipeModel(BaseModel):
    """Validated recipe data."""

    url: str
    gousto_id: Optional[str] = None
    title: str
    slug: Optional[str] = None
    short_title: Optional[str] = None
    description: Optional[str] = None
    marketing_description: Optional[str] = None
    image_url: Optional[str] = None

    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    total_time_minutes: Optional[int] = None

    cuisine: Optional[str] = None
    diet_type: Optional[str] = None
    meal_type: Optional[str] = None
    difficulty: Optional[str] = None

    servings: int = 2
    rating: Optional[Decimal] = None
    rating_count: Optional[int] = None

    ingredients: list[IngredientModel] = Field(default_factory=list)
    cooking_steps: list[CookingStepModel] = Field(default_factory=list)
    nutrition: Optional[NutritionModel] = None
    categories: list[str] = Field(default_factory=list)
    equipment: list[str] = Field(default_factory=list)
    allergens: list[str] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def clean_title(cls, v: str) -> str:
        """Clean up title."""
        return re.sub(r"\s+", " ", v).strip()

    @field_validator("slug", mode="before")
    @classmethod
    def extract_slug(cls, v, info):
        """Extract slug from URL if not provided."""
        if v:
            return v
        url = info.data.get("url", "")
        if url:
            # Extract last path segment
            match = re.search(r"/([^/]+)/?$", url)
            if match:
                return match.group(1)
        return None

    def calculate_total_time(self) -> Optional[int]:
        """Calculate total time from prep and cook times."""
        if self.total_time_minutes:
            return self.total_time_minutes
        if self.prep_time_minutes and self.cook_time_minutes:
            return self.prep_time_minutes + self.cook_time_minutes
        return self.prep_time_minutes or self.cook_time_minutes
