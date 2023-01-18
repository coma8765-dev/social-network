import logging
from datetime import datetime

from app.adapter.pg.repo import PGStorage
from app.domain.entity.users import *
from app.domain.exc import NotFound
from app.domain.repo import users_queries as sql
from app.domain.service.users import UserStorage

logger = logging.getLogger(__name__)


class UserPGStorage(PGStorage, UserStorage):
    async def confirm(self, id_: int):
        raise NotImplemented

    async def create(self, ref: UserRefInner) -> User:
        id_ = await self._db.fetchval(
            sql.CREATE,
            ref.email,
            ref.password_hash,
            ref.name,
        )

        return User(
            id=id_,
            create_date=datetime.now(),
            **ref.dict(),
            confirm=False,
        )

    async def update(self, id_: int, upd: UserUpdateInside):
        if not await self._db.fetchval(
                sql.UPDATE,
                id_,
                upd.name,
                upd.password_hash,
        ):
            logger.warning("User doesn't exists.")

    async def delete(self, id_: int):
        if not await self._db.fetchval(
                sql.DELETE,
                id_,
        ):
            logger.warning("User doesn't exists.")

    async def get(self, id_: int) -> User:
        u = await self._db.fetchrow(sql.GET, id_)

        if not u:
            raise NotFound("user not found")

        return User(**u)

    async def get_user_with_hash_by_email(self, email: str) \
            -> (User, UserPasswordHash):
        u = await self._db.fetchrow(sql.GET_WITH_PWD, email)

        if not u:
            raise NotFound("user not found")

        return User(**u), UserPasswordHash(**u)

    async def email_exists(self, email: str) -> EmailExists:
        return EmailExists(
            exists=await self._db.fetchval(sql.EXISTS, email) is not None,
            email=email,
        )


__all__ = ["UserPGStorage"]
