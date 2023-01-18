from passlib.handlers.bcrypt import bcrypt

from app.domain.provider.password_store.hash import PasswordProvider


class PasswordProviderBcrypt(PasswordProvider):
    @classmethod
    def hash(cls, origin: str) -> str:
        """Get bcrypt password hash"""
        return bcrypt.hash(origin)

    @classmethod
    def verify(cls, hash_, origin) -> bool:
        """Verify bcrypt password hash"""
        return bcrypt.verify(origin, hash_)
