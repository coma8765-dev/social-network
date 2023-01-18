from fastapi import APIRouter, Depends

from app.adapter.jwt.auth import AuthProviderJWT
from app.controller.http.models import HTTPException
from app.domain.entity.users import *
from app.domain.service.users import UserService, UserStorage

router = APIRouter(tags=["auth"])


@router.post("/signin/", status_code=201, response_model=Token)
async def signin(
        ref: Auth,
        repo: UserStorage = Depends(),
):
    user = await UserService(repo).signin(ref)
    return AuthProviderJWT.create_token(user.id)


@router.post(
    "/signup/",
    response_model=User,
    responses={
        400: {
            "description": "Bad Request",
            "model": HTTPException,
            "content": {
                "application/json": {
                    "examples": {
                        "default": {
                            "summary": "Invalid key",
                            "value": {"detail": "Invalid key"},
                        },
                        "email exists": {
                            "summary": "Email exists",
                            "value": {"detail": "Email already exists"},
                        },
                    }
                }
            },
        },
    },
)
async def signup(
        ref: UserRef,
        repo: UserStorage = Depends(),
):
    return await UserService(repo).create(ref)


@router.get("/email_exists/", response_model=EmailExists)
async def email_exists(
        email: str,
        repo: UserStorage = Depends(),
):
    return await UserService(repo).email_exists(email)


@router.get("/user/", response_model=User)
async def me(
        use_case: UserService = Depends(),
):
    return use_case.user


@router.patch("/user/", status_code=204)
async def update(
        upd: UserUpdate,
        use_case: UserService = Depends(),
):
    await use_case.update(upd)


@router.delete("/user/", status_code=204)
async def delete(
        use_case: UserService = Depends(),
):
    await use_case.delete()
