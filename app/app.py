import logging

from fastapi import FastAPI

from app.adapter.pg.session import storage
from app.controller.http import router
from app.controller.http.exc_handler import add_exc_handlers
from app.controller.http.middleware import ExceptionHandlerMiddleware
from app.domain.provider.storage.storage import StorageProvider
from app.domain.repo.posts import PostPGStorage
from app.domain.repo.users import UserPGStorage
from app.domain.service.posts import PostStorage
from app.domain.service.users import UserStorage

logging.basicConfig(level=logging.INFO)

app = FastAPI()

logging.basicConfig(level=logging.WARNING)

app.add_middleware(ExceptionHandlerMiddleware)
add_exc_handlers(app)
app.include_router(router)

app.dependency_overrides[StorageProvider] = storage
app.dependency_overrides[UserStorage] = UserPGStorage
app.dependency_overrides[PostStorage] = PostPGStorage

app.add_event_handler("startup", storage.startup)
