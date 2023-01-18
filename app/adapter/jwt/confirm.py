import logging
from datetime import datetime, timedelta

from jose import jwt

from app.adapter.jwt.jwt import ProviderJWT
from app.domain.provider.confirm.tokens import ConfirmProvider

logger = logging.getLogger(__name__)


class ConfirmProviderJWT(ConfirmProvider, ProviderJWT):
    def get_user_id_by_token(self, token: str) -> int:
        try:
            return jwt.decode(token, self._secret, algorithms=["HS256"])["ac"]
        except (jwt.JWTError, KeyError,) as e:
            logger.exception(f"bad token `{token}`, raised jwt error `{e}`")
            raise self.Exc.bad_token

    def create_token(self, user_id: int) -> str:
        return jwt.encode(
            {"ac": user_id, "exp": datetime.now() + timedelta(days=5)},
            self._secret,
            "HS256"
        )
