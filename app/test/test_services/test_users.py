import os
import random
import unittest
import uuid

import asyncpg
import asyncpg.transaction

from app.adapter.pg.session import StoragePGProvider
from app.domain.entity.users import *
from app.domain.exc import NotFound
from app.domain.repo.users import UserPGStorage
from app.domain.service.users import UserService


class UserTestCase(unittest.IsolatedAsyncioTestCase):
    _tr: asyncpg.transaction.Transaction
    conn: asyncpg.Connection
    repo: UserPGStorage

    @classmethod
    async def asyncSetUp(cls) -> None:
        cls.conn = await asyncpg.connect(StoragePGProvider.conf)
        cls._tr = cls.conn.transaction()
        await cls._tr.start()

        # noinspection PyTypeChecker
        cls.repo = UserPGStorage(cls.conn)

    @classmethod
    async def asyncTearDown(cls) -> None:
        if not os.getenv("TEST_NO_COMMIT", 0):
            await cls._tr.rollback()
        else:
            await cls._tr.commit()

    @classmethod
    def use_case(cls, u: User | None = None) -> UserService:
        return UserService(cls.repo, u)

    @staticmethod
    def _user_ref(**kwargs) -> UserRef:
        return UserRef(
            email=kwargs.pop("email", None) or
            f"{random.randint(1, 100000)}@mail.ru",
            name=kwargs.pop("name", None) or
            f"user-{random.randint(1, 100000)}",
            password=kwargs.pop("password", "test-password"),
            **kwargs,
        )

    async def _user(self, **kwargs) -> User:
        return await self.use_case().create(self._user_ref(**kwargs))

    async def test_create(self):
        use_case = self.use_case()
        key = str(uuid.uuid4())
        ref = self._user_ref(key=key)
        u = await use_case.create(ref)

        self.assertDictEqual(ref.dict(exclude={"password", "key"}),
                             u.dict(exclude={"id", "confirm", "create_date"}))
        self.assertIsInstance(u.id, int)

    async def test_get(self):
        use_case = self.use_case()
        u_ref = await self._user()
        u = await use_case.get(u_ref.id)

        self.assertDictEqual(u_ref.dict(exclude={"create_date"}),
                             u.dict(exclude={"create_date"}))

    async def test_list(self):
        ...

    async def test_signin(self):
        use_case = self.use_case()
        password = "some-password"

        u_ref = await self._user(password=password)

        s = await use_case.signin(Auth(email=u_ref.email, password=password))
        self.assertDictEqual(u_ref.dict(exclude={"create_date"}),
                             s.dict(exclude={"create_date"}))

    async def test_email_exists(self):
        use_case = self.use_case()
        u = await self._user()

        self.assertDictEqual(
            (await use_case.email_exists(u.email)).dict(),
            EmailExists(email=u.email, exists=True).dict(),
        )

        self.assertDictEqual(
            (await use_case.email_exists("no@mail.no")).dict(),
            EmailExists(email="no@mail.no", exists=False).dict(),
        )

    async def test_update(self):
        u = await self._user()
        use_case = self.use_case(u)
        key = str(uuid.uuid4())
        u_new_ref = self._user_ref(key=key)
        upd_ref = UserUpdate(name=u_new_ref.name, password="new_password",
                             icon=uuid.uuid4())

        await use_case.update(upd_ref)
        upd = await use_case.get(u.id)

        self.assertDictEqual(upd_ref.dict(include={"name"}),
                             upd.dict(include={"name"}))
        await use_case.signin(Auth(email=u.email, password=upd_ref.password))

    async def test_delete(self):
        u = await self._user()
        use_case = self.use_case(u)
        await use_case.delete()

        with self.assertRaises(NotFound):
            await use_case.get(u.id)


if __name__ == '__main__':
    unittest.main()
