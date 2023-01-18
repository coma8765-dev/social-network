from asyncpg import Connection
from fastapi import Depends

from app.domain.provider.storage.storage import StorageProvider


class PGStorage:
    __slots__ = "_db"
    _db: Connection

    def __init__(self, db: StorageProvider = Depends()):
        self._db = db
