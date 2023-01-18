from fastapi import APIRouter

from .routes.available import router as available_router
from .routes.users import router as auth_router
from .routes.posts import router as post_router

router = APIRouter(prefix="/v1")

router.include_router(available_router)
router.include_router(auth_router)
router.include_router(post_router)
