"""
Async engine for SqlAlchemy
"""
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine as _create_async_engine
)
from sqlalchemy.orm import sessionmaker

from bot.settings import POSTGRES_URL


def create_async_engine(url: URL | str) -> AsyncEngine:
    """
    Create async engine with constant params
    :param url:
    :return:
    """
    return _create_async_engine(url=url, echo=True, pool_pre_ping=True)


async def get_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    """
    return async session maker
    :param engine:
    :return:
    """
    return async_sessionmaker(engine, class_=AsyncSession)
    # return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


engine = create_async_engine(POSTGRES_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

async def get_async_session():
    """
    Returns async session for FastAPI Dependency Injections.
    """
    async with AsyncSessionLocal() as async_session:
        yield async_session
