from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine as _create_async_engine
)
from sqlalchemy.engine.url import URL

def create_async_engine(url: URL | str) -> AsyncEngine:
    return _create_async_engine(url=url, echo=True, pool_pre_ping=True)

async def proceed_schemas(engine: AsyncEngine, metadata) -> None:
    async with engine.connect() as conn:
        await conn.run_sync(metadata.create_all)

async def get_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

