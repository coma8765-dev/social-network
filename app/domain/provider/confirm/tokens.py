from abc import ABC, abstractmethod


class ConfirmProvider(ABC):
    @abstractmethod
    def get_user_id_by_token(self, token: str) -> int: ...

    @abstractmethod
    def create_token(self, user_id: int) -> str: ...
