# Gousto Recipe Database Scraper

## Project Overview

Build a Python application to scrape all recipes from https://www.gousto.co.uk/cookbook/recipes and store them in a structured database with complete recipe information including ingredients, nutritional data, and cooking instructions.

## Technical Requirements

### Technology Stack
- **Language**: Python 3.11+
- **Web Scraping**: Playwright or Selenium (required - site is JavaScript-rendered)
- **HTTP Client**: httpx or aiohttp for any direct API calls
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy 2.0+ with async support
- **Data Validation**: Pydantic v2

### Alternative Approach
Consider using the `recipe-scrapers` library (https://pypi.org/project/recipe-scrapers/) which has Gousto support, combined with Playwright for pagination handling.

## Database Schema

Design a normalized database with the following tables:

### Core Tables

```sql
-- Recipes table
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gousto_id VARCHAR(50) UNIQUE,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE,
    short_title VARCHAR(255),
    description TEXT,
    marketing_description TEXT,
    image_url TEXT,

    -- Timing
    prep_time_minutes INTEGER,
    cook_time_minutes INTEGER,
    total_time_minutes INTEGER,

    -- Classification
    cuisine VARCHAR(100),
    diet_type VARCHAR(100),  -- vegetarian, vegan, meat, fish
    meal_type VARCHAR(100),  -- breakfast, lunch, dinner
    difficulty VARCHAR(50),

    -- Servings
    servings INTEGER DEFAULT 2,

    -- Metadata
    rating DECIMAL(3,2),
    rating_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Nutritional information (per serving)
CREATE TABLE nutrition (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL UNIQUE,
    calories_kcal INTEGER,
    protein_grams DECIMAL(6,2),
    fat_grams DECIMAL(6,2),
    saturated_fat_grams DECIMAL(6,2),
    carbs_grams DECIMAL(6,2),
    sugar_grams DECIMAL(6,2),
    fibre_grams DECIMAL(6,2),
    salt_grams DECIMAL(6,2),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- Ingredients
CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    quantity VARCHAR(100),
    unit VARCHAR(50),
    preparation_note VARCHAR(255),  -- "finely chopped", "diced"
    is_optional BOOLEAN DEFAULT FALSE,
    display_order INTEGER,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- Cooking steps/instructions
CREATE TABLE cooking_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    step_number INTEGER NOT NULL,
    instruction TEXT NOT NULL,
    duration_minutes INTEGER,
    tip TEXT,
    image_url TEXT,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- Recipe categories/tags (many-to-many)
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    category_type VARCHAR(50)  -- cuisine, dietary, meal-type, season
);

CREATE TABLE recipe_categories (
    recipe_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (recipe_id, category_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Equipment needed
CREATE TABLE equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE recipe_equipment (
    recipe_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    PRIMARY KEY (recipe_id, equipment_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (equipment_id) REFERENCES equipment(id) ON DELETE CASCADE
);

-- Allergens
CREATE TABLE allergens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE recipe_allergens (
    recipe_id INTEGER NOT NULL,
    allergen_id INTEGER NOT NULL,
    contains BOOLEAN DEFAULT TRUE,  -- TRUE = contains, FALSE = may contain
    PRIMARY KEY (recipe_id, allergen_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (allergen_id) REFERENCES allergens(id) ON DELETE CASCADE
);
```

## Implementation Structure

```
src/
├── __init__.py
├── main.py                 # Entry point
├── config.py               # Configuration settings
├── database/
│   ├── __init__.py
│   ├── models.py           # SQLAlchemy models
│   ├── connection.py       # Database connection
│   └── migrations/         # Alembic migrations
├── scrapers/
│   ├── __init__.py
│   ├── base.py             # Base scraper class
│   ├── gousto_scraper.py   # Main Gousto scraper
│   ├── recipe_parser.py    # Parse individual recipes
│   └── pagination.py       # Handle infinite scroll/pagination
├── models/
│   ├── __init__.py
│   └── recipe.py           # Pydantic models for validation
├── utils/
│   ├── __init__.py
│   ├── rate_limiter.py     # Respectful rate limiting
│   ├── retry.py            # Retry logic with backoff
│   └── logging.py          # Logging configuration
└── exporters/
    ├── __init__.py
    ├── json_exporter.py
    └── csv_exporter.py
```

## Scraping Strategy

### Phase 1: Discovery
1. Navigate to https://www.gousto.co.uk/cookbook/recipes
2. Handle JavaScript rendering with Playwright
3. Scroll/paginate to load all recipes (site uses infinite scroll or "Load More")
4. Extract all recipe URLs from listing pages
5. Store URLs in a queue for processing

### Phase 2: Recipe Extraction
For each recipe URL, extract:

1. **Basic Info**
   - Title, slug, description
   - Hero image URL
   - Rating and review count

2. **Timing & Difficulty**
   - Prep time, cook time, total time
   - Difficulty level
   - Servings

3. **Ingredients** (parse structured data)
   - Ingredient name
   - Quantity and unit
   - Preparation notes

4. **Cooking Steps**
   - Step-by-step instructions
   - Step images if available
   - Tips for each step

5. **Nutrition** (per serving)
   - Calories, protein, fat, carbs
   - Additional: fibre, salt, sugar, saturated fat

6. **Categories/Tags**
   - Cuisine type (Asian, Italian, etc.)
   - Dietary info (vegetarian, vegan, dairy-free)
   - Meal type (quick meals, family, date night)

7. **Additional Data**
   - Equipment needed
   - Allergen information
   - "In your box" items vs pantry staples

### Rate Limiting & Politeness
- Implement 2-3 second delays between requests
- Respect robots.txt
- Use exponential backoff on failures
- Set appropriate User-Agent header
- Consider running during off-peak hours

## Pydantic Models

```python
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional

class Ingredient(BaseModel):
    name: str
    quantity: Optional[str] = None
    unit: Optional[str] = None
    preparation_note: Optional[str] = None
    is_optional: bool = False

class CookingStep(BaseModel):
    step_number: int
    instruction: str
    duration_minutes: Optional[int] = None
    tip: Optional[str] = None
    image_url: Optional[str] = None

class Nutrition(BaseModel):
    calories_kcal: Optional[int] = None
    protein_grams: Optional[Decimal] = None
    fat_grams: Optional[Decimal] = None
    saturated_fat_grams: Optional[Decimal] = None
    carbs_grams: Optional[Decimal] = None
    sugar_grams: Optional[Decimal] = None
    fibre_grams: Optional[Decimal] = None
    salt_grams: Optional[Decimal] = None

class Recipe(BaseModel):
    gousto_id: str
    title: str
    slug: str
    description: Optional[str] = None
    image_url: Optional[str] = None

    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    total_time_minutes: Optional[int] = None

    cuisine: Optional[str] = None
    diet_type: Optional[str] = None
    difficulty: Optional[str] = None
    servings: int = 2

    rating: Optional[Decimal] = None
    rating_count: Optional[int] = None

    ingredients: list[Ingredient] = Field(default_factory=list)
    cooking_steps: list[CookingStep] = Field(default_factory=list)
    nutrition: Optional[Nutrition] = None
    categories: list[str] = Field(default_factory=list)
    equipment: list[str] = Field(default_factory=list)
    allergens: list[str] = Field(default_factory=list)
```

## Key Implementation Notes

### JavaScript Rendering
The Gousto site is a React SPA requiring JavaScript execution:

```python
from playwright.async_api import async_playwright

async def scrape_recipe_list():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://www.gousto.co.uk/cookbook/recipes")

        # Wait for recipes to load
        await page.wait_for_selector("[data-testid='recipe-card']", timeout=10000)

        # Scroll to load all recipes (infinite scroll)
        previous_count = 0
        while True:
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)

            recipe_cards = await page.query_selector_all("[data-testid='recipe-card']")
            current_count = len(recipe_cards)

            if current_count == previous_count:
                break
            previous_count = current_count

        # Extract URLs
        recipe_urls = await page.evaluate('''
            () => Array.from(document.querySelectorAll('a[href*="/cookbook/"]'))
                       .map(a => a.href)
                       .filter(href => href.includes('-recipes/'))
        ''')

        await browser.close()
        return list(set(recipe_urls))
```

### Using recipe-scrapers Library
For individual recipe parsing, leverage existing library:

```python
from recipe_scrapers import scrape_html
import httpx

async def parse_recipe(url: str, html: str) -> dict:
    scraper = scrape_html(html, url)

    return {
        "title": scraper.title(),
        "ingredients": scraper.ingredients(),
        "instructions": scraper.instructions(),
        "nutrients": scraper.nutrients(),
        "image": scraper.image(),
        "yields": scraper.yields(),
        "total_time": scraper.total_time(),
        "cook_time": scraper.cook_time(),
        "prep_time": scraper.prep_time(),
    }
```

## Execution Plan

1. **Setup** (Phase 1)
   - Create project structure
   - Set up virtual environment with dependencies
   - Configure database and run migrations
   - Create logging infrastructure

2. **URL Discovery** (Phase 2)
   - Scrape all recipe listing pages
   - Handle pagination/infinite scroll
   - Store unique recipe URLs (~1000+ recipes expected)

3. **Recipe Scraping** (Phase 3)
   - Process each URL with rate limiting
   - Parse and validate data with Pydantic
   - Handle errors gracefully with retry logic
   - Save to database incrementally

4. **Data Validation** (Phase 4)
   - Verify data completeness
   - Check for duplicates
   - Validate nutrition data ranges
   - Generate data quality report

5. **Export** (Phase 5)
   - Provide JSON export functionality
   - Provide CSV export for spreadsheet use
   - Optional: SQLite file for portability

## Dependencies

```txt
# requirements.txt
playwright>=1.40.0
httpx>=0.25.0
sqlalchemy>=2.0.0
pydantic>=2.5.0
alembic>=1.13.0
aiosqlite>=0.19.0  # For async SQLite
asyncpg>=0.29.0    # For PostgreSQL
recipe-scrapers>=14.50.0
tenacity>=8.2.0    # Retry logic
loguru>=0.7.0      # Better logging
rich>=13.0.0       # Progress bars
```

## Ethical Considerations

- Only scrape publicly available recipe data
- Implement respectful rate limiting (2-3 sec delays)
- Check and respect robots.txt
- Do not store personal user data
- Consider caching to avoid repeated requests
- Use data for personal/educational purposes only
- Attribution: Credit Gousto as the data source

## Expected Output

- SQLite database with ~1000+ recipes
- Complete ingredient lists with quantities
- Full cooking instructions
- Nutritional information per serving
- Category/tag classifications
- Equipment requirements
- JSON/CSV export options

## Success Criteria

- [ ] All accessible recipes scraped and stored
- [ ] No duplicate recipes in database
- [ ] All required fields populated where available
- [ ] Nutrition data validated for realistic ranges
- [ ] Export functionality working for JSON/CSV
- [ ] Comprehensive error logging
- [ ] Rate limiting respected throughout
