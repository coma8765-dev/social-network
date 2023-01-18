import os

from app.domain.exc import BadRequest


class ProviderJWT:
    _secret = os.getenv("JWT_SECRET", "1234567890")

    class Exc:
        bad_token = BadRequest("bad token")
