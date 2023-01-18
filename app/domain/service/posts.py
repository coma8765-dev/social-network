from abc import ABC, abstractmethod

from fastapi import Depends

from app.domain.entity.posts import *
from app.domain.entity.users import User
from app.domain.exc import AccessDenied, BadRequest
from app.domain.service.users import get_user


class PostStorage(ABC):
    @abstractmethod
    async def create(self, user_id: int, ref: PostRef) -> Post: ...

    @abstractmethod
    async def delete(self, id_: int): ...

    @abstractmethod
    async def update(self, id_: int, ref: PostUpdate): ...

    @abstractmethod
    async def get(self, id_: int, user_id: int) -> Post: ...

    @abstractmethod
    async def estimate(
            self,
            id_: int,
            user_id: int,
            ref: PostEstimate,
    ): ...

    @abstractmethod
    async def list(self, user_id: int, params: PostFilter) -> PostList: ...


class PostService:
    __slots__ = "__repo", "__user",
    __repo: PostStorage
    __user: User

    def __init__(
            self,
            repo: PostStorage = Depends(),
            user: User = Depends(get_user),
    ):
        self.__repo = repo
        self.__user = user

    async def create(self, ref: PostRef) -> Post:
        return await self.__repo.create(self.__user.id, ref)

    async def get(self, id_: int) -> Post:
        return await self.__repo.get(id_, self.__user.id)

    async def list(self, params: PostFilter) -> PostList:
        return await self.__repo.list(self.__user.id, params)

    async def __modifier_can_edit(self, id_: int):
        post = await self.__repo.get(id_, self.__user.id)

        if post.created_by != self.__user.id:
            raise AccessDenied(f"You cannot edit post with id {id_}")

    async def update(self, id_: int, ref: PostUpdate):
        await self.__modifier_can_edit(id_)
        await self.__repo.update(id_, ref)

    async def delete(self, id_: int):
        await self.__modifier_can_edit(id_)
        await self.__repo.delete(id_)

    async def estimate(
            self,
            id_: int,
            ref: PostEstimate,
    ):
        post = await self.__repo.get(id_, self.__user.id)

        if post.created_by == self.__user.id:
            raise BadRequest(
                "The author of the message cannot evaluate his post",
            )

        await self.__repo.estimate(id_, self.__user.id, ref)
