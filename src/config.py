"""Configuration settings for the Gousto recipe scraper."""

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Database
    database_url: str = "sqlite+aiosqlite:///./gousto_recipes.db"

    # Scraping
    base_url: str = "https://www.gousto.co.uk"
    cookbook_url: str = "https://www.gousto.co.uk/cookbook/recipes"
    request_delay_seconds: float = 2.5
    max_retries: int = 3
    timeout_seconds: int = 30

    # Browser settings
    headless: bool = True
    slow_mo: int = 100  # milliseconds between actions

    # Paths
    project_root: Path = Path(__file__).parent.parent
    data_dir: Path = project_root / "data"
    logs_dir: Path = project_root / "logs"

    # Export settings
    export_dir: Path = project_root / "exports"

    class Config:
        env_prefix = "GOUSTO_"


settings = Settings()

# Ensure directories exist
settings.data_dir.mkdir(exist_ok=True)
settings.logs_dir.mkdir(exist_ok=True)
settings.export_dir.mkdir(exist_ok=True)
