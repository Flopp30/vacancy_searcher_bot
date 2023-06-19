"""
Async engine for SqlAlchemy
"""
from contextlib import asynccontextmanager

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine as _create_async_engine
)
from sqlalchemy.orm import sessionmaker

from .settings import POSTGRES_URL


def create_async_engine(url: URL | str) -> AsyncEngine:
    """
    Create async engine with constant params
    :param url:
    :return:
    """
    return _create_async_engine(url=url, pool_pre_ping=True)


engine = create_async_engine(POSTGRES_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """
    Returns async session for FastAPI Dependency Injections.
    """
    async with AsyncSessionLocal() as async_session:
        try:
            yield async_session
        finally:
            await async_session.close()


@asynccontextmanager
async def bot_get_async_session():
    async with AsyncSessionLocal() as async_session:
        try:
            yield async_session
        finally:
            await async_session.close()
