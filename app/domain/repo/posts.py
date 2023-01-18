import logging

from app.adapter.pg.repo import PGStorage
from app.domain.entity.posts import *
from app.domain.exc import NotFound
from app.domain.repo import posts_queries as sql
from app.domain.service.posts import PostStorage

logger = logging.getLogger(__name__)


LIMIT_PER_PAGE = 10


class PostPGStorage(PGStorage, PostStorage):
    async def create(self, user_id: int, ref: PostRef) -> Post:
        res = await self._db.fetchrow(
            sql.CREATE,
            user_id,
            ref.title,
            ref.body,
        )

        return Post(**res, **ref.dict(), created_by=user_id)

    async def delete(self, id_: int):
        if await self._db.fetchval(sql.DELETE, id_) is None:
            raise NotFound("Post not found")

    async def update(self, id_: int, ref: PostUpdate):
        if await self._db.fetchval(
                sql.UPDATE,
                id_,
                ref.title,
                ref.body,
        ) is None:
            raise NotFound("Post not found")

    async def get(self, id_: int, user_id: int) -> Post:
        res = await self._db.fetchrow(sql.GET, id_, user_id)

        if res is None:
            raise NotFound("Post not found")
        return Post(**res)

    async def list(self, user_id: int, params: PostFilter) -> PostList:
        res = await self._db.fetch(
            sql.LIST,
            params.page - 1,  # Page
            LIMIT_PER_PAGE,  # Limit
            user_id,
            # params.title,  # TODO: Implement
        )

        return PostList(
            page=params.page,
            has_next=len(res) == LIMIT_PER_PAGE + 1,
            list=res[:LIMIT_PER_PAGE],
        )

    async def estimate(
            self,
            id_: int,
            user_id: int,
            ref: PostEstimate,
    ):
        if ref.clear:
            await self._db.execute(
                sql.REMOVE_ESTIMATE,
                id_,
                user_id,
            )
        else:
            await self._db.execute(
                sql.ESTIMATE,
                id_,
                user_id,
                ref.positive,
            )


__all__ = ["PostPGStorage"]
