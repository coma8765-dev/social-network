from abc import ABC, abstractmethod

from fastapi import Depends

from app.adapter.bcrypt.passwords import PasswordProviderBcrypt
from app.adapter.jwt.auth import AuthProviderJWT
from app.adapter.jwt.confirm import ConfirmProviderJWT
from app.domain.entity.users import *
from app.domain.exc import NotFound, BadRequest


class UserStorage(ABC):
    @abstractmethod
    async def create(self, ref: UserRefInner) -> User: ...

    @abstractmethod
    async def update(self, id_: int, upd: UserUpdateInside): ...

    @abstractmethod
    async def delete(self, id_: int): ...

    @abstractmethod
    async def get(self, id_: int) -> User: ...

    @abstractmethod
    async def get_user_with_hash_by_email(self, email: str) \
            -> (User, UserPasswordHash):
        ...

    @abstractmethod
    async def confirm(self, id_: int): ...

    @abstractmethod
    async def email_exists(self, email: str) -> EmailExists: ...


async def get_user(
        user_id: int | None = Depends(AuthProviderJWT.dependency),
        repo: UserStorage = Depends(UserStorage),
):
    return user_id and await repo.get(user_id)


class UserService:
    """Service for work with user

    Examples:
        * Create service instance:
            ```python
                document_repo = UserPGStorage(db)
                user = document_repo.get(user_id)  # Optional, maybe None
                use_case = UserService(document_repo, user)
            ```
    Todo:
        * add confirm by email
        * add update email
    """
    __slots__ = "repo", "user",
    repo: UserStorage
    user: User | None

    password_provider = PasswordProviderBcrypt()
    confirm_provider = ConfirmProviderJWT()

    def __init__(
            self,
            repo: UserStorage = Depends(),
            user: User | None = Depends(get_user),
    ):
        self.repo = repo
        self.user = user

    async def create(self, ref: UserRef) -> User:
        """Creates new user

        Args:
            ref: Data for creating a new user.
        Returns:
            New user
            Warning: `create_date` not equal `create_date` from db.
        Raises:
            BadRequest: If email already exists.
        """
        if await self.email_exists(ref.email):
            raise BadRequest("email already exists")

        return await self.repo.create(UserRefInner(
            **ref.dict(),
            password_hash=self.password_provider.hash(ref.password),
        ))

    async def signin(self, ref: Auth) -> User:
        """Returns the user by login refs

        Args:
            ref: Data fot authorization
        Returns:
            User
        Raises:
            NotFound: if email or password invalid
        """
        user, pwd_hash = await self.repo.get_user_with_hash_by_email(ref.email)

        if self.password_provider.verify(
                pwd_hash.password_hash,
                ref.password,
        ):
            return user

        raise NotFound("user not found")

    async def confirm(self, token: str):
        """Email confirm

        Args:
            token: Confirm token
        """
        user_id = self.confirm_provider.get_user_id_by_token(token)
        await self.repo.confirm(user_id)

    async def confirm_send(self, id_: int):
        """Email confirm

        Send email on user email with confirm token
        Args:
            id_: User id
        """
        raise NotImplemented

    async def email_exists(self, email: str) -> EmailExists:
        """Returns email exists

        Args:
            email: Desired email
        Returns:
            Email exists model
        """
        return await self.repo.email_exists(email)

    async def update(self, upd: UserUpdate):
        """Updates the user

        Args:
            upd: Update data
        """
        await self.repo.update(
            self.user.id,
            UserUpdateInside(
                **upd.dict(),
                password_hash=upd.password and self.password_provider.hash(
                    upd.password) or None
            )
        )

    async def delete(self):
        """Deletes a user"""
        await self.repo.delete(self.user.id)

    async def get(self, id_: int) -> User:
        """Returns user

        Args:
            id_: User id
        Returns:
            User
        Raises:
            NotFound: If user doesn't exist
        """
        return await self.repo.get(id_)

    async def list(self, params: UserFilter | None = None) -> UserList:
        raise NotImplemented
