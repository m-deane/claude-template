"""Database connection management."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.database.models import Base


def get_engine():
    """Create async database engine."""
    return create_async_engine(
        settings.database_url,
        echo=False,
        future=True,
    )


def get_session_factory(engine) -> async_sessionmaker[AsyncSession]:
    """Create session factory."""
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def init_db(engine=None):
    """Initialize database tables."""
    if engine is None:
        engine = get_engine()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session."""
    engine = get_engine()
    session_factory = get_session_factory(engine)

    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
