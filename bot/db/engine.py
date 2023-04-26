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


def create_async_engine(url: URL | str) -> AsyncEngine:
    """
    Create async engine with constant params
    :param url:
    :return:
    """
    return _create_async_engine(url=url, echo=True, pool_pre_ping=True)


# TODO выпилить после подключения alembic
async def proceed_schemas(engine: AsyncEngine, metadata) -> None:
    """
    После подключения alembic выпилить надо будет.
    :param engine:
    :param metadata:
    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


async def get_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    """
    return async session maker
    :param engine:
    :return:
    """
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
