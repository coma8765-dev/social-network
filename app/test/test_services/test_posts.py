import os
import random
import unittest

import asyncpg
import asyncpg.transaction

from app.adapter.pg.session import StoragePGProvider
from app.domain.entity.users import UserRef
from app.domain.entity.posts import *
from app.domain.repo.posts import PostPGStorage
from app.domain.repo.users import UserPGStorage
from app.domain.service.posts import PostService
from app.domain.service.users import UserService


class PostTestCase(unittest.IsolatedAsyncioTestCase):
    _tr: asyncpg.transaction.Transaction
    conn: asyncpg.Connection
    repo: PostPGStorage
    user_use_case: UserService

    @classmethod
    async def asyncSetUp(cls) -> None:
        cls.conn = await asyncpg.connect(StoragePGProvider.conf)
        cls._tr = cls.conn.transaction()
        await cls._tr.start()

        # noinspection PyTypeChecker
        cls.repo = PostPGStorage(cls.conn)
        # noinspection PyTypeChecker
        cls.user_use_case = UserService(UserPGStorage(cls.conn))

    @classmethod
    async def asyncTearDown(cls) -> None:
        if not os.getenv("TEST_NO_COMMIT", 0):
            await cls._tr.rollback()
        else:
            await cls._tr.commit()

    @property
    async def use_case(self) -> PostService:
        user = await self.user_use_case.create(UserRef(
            email=f"{random.randint(1, 100000)}@mail.ru",
            name=f"user-{random.randint(1, 100000)}",
            password="test-password",
        ))

        return PostService(self.repo, user)

    async def create_post(
            self,
            use_case: PostService | None = None,
            ref: PostRef | None = None,
    ):
        if use_case is None:
            use_case = await self.use_case

        return await use_case.create(ref or PostRef(
            title="some title",
            body="some body",
        ))

    async def test_create(self):
        ref = PostRef(
            title=f"post-{random.randint(0, 1000000000)}",
            body=f"post-{random.randint(0, 1000000000)}",
        )

        post = await self.create_post(ref=ref)

        self.assertDictEqual(
            post.dict(include=ref.__fields_set__),
            ref.dict(),
        )

    async def test_get(self):
        use_case = await self.use_case
        post_ref = await self.create_post(use_case)
        post = await use_case.get(post_ref.id)

        self.assertDictEqual(
            post_ref.dict(exclude={"create_date"}),
            post.dict(exclude={"create_date"}),
        )

    async def test_list(self): ...

    async def test_update(self): ...

    async def test_delete(self): ...


if __name__ == '__main__':
    unittest.main()
