import asyncio
from typing import AsyncGenerator, Generator, Never

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine, text

from it_co_test.config import DB_URL
from it_co_test.db.models import Base


@pytest_asyncio.fixture(autouse=True)
async def clean_tables(sync_engine: Engine) -> AsyncGenerator:
    yield
    table_names = ["project"]
    tables_str = ", ".join(table_names)
    command = f"TRUNCATE TABLE {tables_str};"
    with sync_engine.connect() as connection:
        connection.execute(text(command))
        connection.commit()


@pytest.fixture(scope="session")
def event_loop(request: Never) -> Generator:
    assert request
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def sync_engine(sync_url: str) -> Engine:
    engine = create_engine(sync_url)
    return engine


@pytest.fixture(scope="session")
def sync_url() -> str:
    return "postgresql:" + ":".join(DB_URL.split(":")[1:])


@pytest.fixture(scope="session")
def load_dotenv_() -> None:
    load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def create_tables(sync_engine: Engine) -> None:
    Base.metadata.create_all(sync_engine)
