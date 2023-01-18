from abc import ABC, abstractmethod

from fastapi import Header

from app.domain.entity.users import Token
from app.domain.exc import BadRequest


class AuthProvider(ABC):
    @classmethod
    @abstractmethod
    def get_user_id_by_token(cls, token: str) -> int: ...

    @classmethod
    @abstractmethod
    def create_token(cls, user_id: int) -> Token: ...

    @classmethod
    def dependency(cls, token: str | None = None, authorization: str | None = Header(None)) -> int | None:
        """Returns user id using get user_id_by_token method"""
        if token is None and authorization is None:
            return

        # Future decline token without "Bearer" header
        if authorization and len(authorization.split()) == 2:
            authorization = authorization.split()[1]

        return cls.get_user_id_by_token(
            authorization or token
        )
