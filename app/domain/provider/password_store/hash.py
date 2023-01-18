from abc import ABC, abstractmethod


class PasswordProvider(ABC):
    @classmethod
    @abstractmethod
    def hash(cls, origin: str) -> str: ...

    @classmethod
    @abstractmethod
    def verify(cls, hash_, origin) -> bool: ...
