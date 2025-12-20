"""SQLAlchemy database models for Gousto recipes."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
    Text,
    Column,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


# Association tables for many-to-many relationships
recipe_categories = Table(
    "recipe_categories",
    Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)

recipe_equipment = Table(
    "recipe_equipment",
    Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True),
    Column("equipment_id", Integer, ForeignKey("equipment.id", ondelete="CASCADE"), primary_key=True),
)

recipe_allergens = Table(
    "recipe_allergens",
    Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True),
    Column("allergen_id", Integer, ForeignKey("allergens.id", ondelete="CASCADE"), primary_key=True),
    Column("contains", Boolean, default=True),  # True = contains, False = may contain
)


class Recipe(Base):
    """Main recipe table."""

    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    gousto_id: Mapped[Optional[str]] = mapped_column(String(100), unique=True, nullable=True)
    url: Mapped[str] = mapped_column(String(500), unique=True)
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    short_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    marketing_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timing
    prep_time_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    cook_time_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_time_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Classification
    cuisine: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    diet_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    meal_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    difficulty: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Servings
    servings: Mapped[int] = mapped_column(Integer, default=2)

    # Ratings
    rating: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 2), nullable=True)
    rating_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Metadata
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    scraped_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    nutrition: Mapped[Optional["Nutrition"]] = relationship(
        "Nutrition", back_populates="recipe", uselist=False, cascade="all, delete-orphan"
    )
    ingredients: Mapped[list["Ingredient"]] = relationship(
        "Ingredient", back_populates="recipe", cascade="all, delete-orphan", order_by="Ingredient.display_order"
    )
    cooking_steps: Mapped[list["CookingStep"]] = relationship(
        "CookingStep", back_populates="recipe", cascade="all, delete-orphan", order_by="CookingStep.step_number"
    )
    categories: Mapped[list["Category"]] = relationship(
        "Category", secondary=recipe_categories, back_populates="recipes"
    )
    equipment_items: Mapped[list["Equipment"]] = relationship(
        "Equipment", secondary=recipe_equipment, back_populates="recipes"
    )
    allergen_items: Mapped[list["Allergen"]] = relationship(
        "Allergen", secondary=recipe_allergens, back_populates="recipes"
    )

    def __repr__(self) -> str:
        return f"<Recipe(id={self.id}, title='{self.title}')>"


class Nutrition(Base):
    """Nutritional information per serving."""

    __tablename__ = "nutrition"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"), unique=True)

    calories_kcal: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    protein_grams: Mapped[Optional[Decimal]] = mapped_column(Numeric(6, 2), nullable=True)
    fat_grams: Mapped[Optional[Decimal]] = mapped_column(Numeric(6, 2), nullable=True)
    saturated_fat_grams: Mapped[Optional[Decimal]] = mapped_column(Numeric(6, 2), nullable=True)
    carbs_grams: Mapped[Optional[Decimal]] = mapped_column(Numeric(6, 2), nullable=True)
    sugar_grams: Mapped[Optional[Decimal]] = mapped_column(Numeric(6, 2), nullable=True)
    fibre_grams: Mapped[Optional[Decimal]] = mapped_column(Numeric(6, 2), nullable=True)
    salt_grams: Mapped[Optional[Decimal]] = mapped_column(Numeric(6, 2), nullable=True)

    # Relationship
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="nutrition")

    def __repr__(self) -> str:
        return f"<Nutrition(recipe_id={self.recipe_id}, calories={self.calories_kcal})>"


class Ingredient(Base):
    """Recipe ingredients."""

    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"))

    name: Mapped[str] = mapped_column(String(255))
    quantity: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    unit: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    raw_text: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    preparation_note: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_optional: Mapped[bool] = mapped_column(Boolean, default=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0)

    # Relationship
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="ingredients")

    def __repr__(self) -> str:
        return f"<Ingredient(id={self.id}, name='{self.name}')>"


class CookingStep(Base):
    """Cooking instructions/steps."""

    __tablename__ = "cooking_steps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id", ondelete="CASCADE"))

    step_number: Mapped[int] = mapped_column(Integer)
    instruction: Mapped[str] = mapped_column(Text)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tip: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationship
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="cooking_steps")

    def __repr__(self) -> str:
        return f"<CookingStep(recipe_id={self.recipe_id}, step={self.step_number})>"


class Category(Base):
    """Recipe categories/tags."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    category_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Relationship
    recipes: Mapped[list["Recipe"]] = relationship(
        "Recipe", secondary=recipe_categories, back_populates="categories"
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"


class Equipment(Base):
    """Kitchen equipment needed."""

    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    # Relationship
    recipes: Mapped[list["Recipe"]] = relationship(
        "Recipe", secondary=recipe_equipment, back_populates="equipment_items"
    )

    def __repr__(self) -> str:
        return f"<Equipment(id={self.id}, name='{self.name}')>"


class Allergen(Base):
    """Allergen information."""

    __tablename__ = "allergens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    # Relationship
    recipes: Mapped[list["Recipe"]] = relationship(
        "Recipe", secondary=recipe_allergens, back_populates="allergen_items"
    )

    def __repr__(self) -> str:
        return f"<Allergen(id={self.id}, name='{self.name}')>"
