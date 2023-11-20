import os

DB_URL = os.getenv(
    "DB_URL", "postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres"
)
