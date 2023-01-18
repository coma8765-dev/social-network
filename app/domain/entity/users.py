import uuid

from pydantic import BaseModel, constr

from app.domain.entity.base import ListDTO


class Email(BaseModel):
    """Email field"""
    email: str


class EmailExists(Email):
    """Email exists field"""
    exists: bool

    def __bool__(self):
        return self.exists


class UserBaseSecondary(Email):
    """Secondary user model for signup"""
    name: str


class User(UserBaseSecondary):
    """Full user model"""
    id: int


class UserPassword(BaseModel):
    """Password field"""
    password: str


class UserPasswordHash(BaseModel):
    """Hash password field"""
    password_hash: constr(min_length=60, max_length=60)


class Auth(Email, UserPassword):
    """Authentication model"""
    pass


class UserRef(UserBaseSecondary, UserPassword):
    """A model for creating a user"""
    pass


class UserRefInner(UserBaseSecondary, UserPasswordHash):
    """Internal model for creating a user"""
    pass


class UserUpdate(BaseModel):
    """The model for updating the user"""
    name: str | None
    # email: str | None
    # TODO(future): Add an email field for updating,
    #  when using set confirm false
    password: str | None
    icon: uuid.UUID | None


class UserUpdateInside(UserUpdate):
    """Internal model for updating the user"""
    password_hash: str | None


class UserFilter(BaseModel):
    """A model for filtering users"""
    email: str | None
    name: str | None


class UserList(ListDTO):
    """User pagination model"""
    list: list[User]


class Token(BaseModel):
    """Token model"""
    type: str = "Bearer"
    token: str


__all__ = [
    "User", "UserRef", "UserUpdate", "Auth", "EmailExists",
    "UserRefInner", "UserUpdateInside", "UserPasswordHash",
    "Token", "UserFilter", "UserList",
]
