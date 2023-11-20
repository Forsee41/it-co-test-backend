from collections.abc import AsyncGenerator
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from it_co_test.config import DB_URL

engine = create_async_engine(url=DB_URL)
db_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession  # type: ignore
)


async def session() -> AsyncGenerator[None, Type]:
    session = db_session()
    yield session
    await session.close()
