import logging
import os

import asyncpg

from app.domain.provider.storage.storage import StorageProvider

logger = logging.getLogger(__name__)


class StoragePGProvider(StorageProvider):
    pool: asyncpg.Pool
    conf = f"postgresql://" \
           f"{os.getenv('POSTGRES_USER', None) or 'postgres'}:" \
           f"{os.getenv('POSTGRES_PASSWORD', None) or 'password'}@" \
           f"{os.getenv('POSTGRES_HOST', None) or 'localhost'}:" \
           f"{os.getenv('POSTGRES_PORT', None) or 5432}/" \
           f"{os.getenv('POSTGRES_DATABASE', None) or 'postgres'}"

    async def startup(self):
        self.pool = await asyncpg.create_pool(self.conf)

    async def __call__(self) -> asyncpg.Connection:
        async with self.pool.acquire() as conn:
            conn: asyncpg.Connection

            logger.debug("use db transaction")

            async with conn.transaction():
                yield conn


storage = StoragePGProvider()
