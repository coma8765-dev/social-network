import logging
from datetime import datetime, timedelta

from jose import jwt

from app.adapter.jwt.jwt import ProviderJWT
from app.domain.entity.users import Token
from app.domain.provider.auth.tokens import AuthProvider

logger = logging.getLogger(__name__)


class AuthProviderJWT(AuthProvider, ProviderJWT):
    @classmethod
    def get_user_id_by_token(cls, token: str) -> int:
        try:
            return int(jwt.decode(token, cls._secret, algorithms=["HS256"])["a"])
        except (jwt.JWTError, KeyError) as e:
            logger.exception(f"bad token `{token}`, raised jwt error `{e}`")
            raise cls.Exc.bad_token

    @classmethod
    def create_token(cls, user_id: int) -> Token:
        token = jwt.encode(
            {"a": user_id, "exp": datetime.now() + timedelta(days=90)},
            cls._secret,
            "HS256"
        )

        return Token(token=token)
