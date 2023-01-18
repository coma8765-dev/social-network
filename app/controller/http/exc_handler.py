import logging

from fastapi import FastAPI
from starlette.responses import JSONResponse, Response

from app.domain.exc import BadRequest, NotAuth, NotFound, PositionNonExists

logger = logging.getLogger("app.exc")


def add_exc_handlers(app: FastAPI):
    app.add_exception_handler(BadRequest, bad_request_handler)
    app.add_exception_handler(NotFound, not_found_handler)
    app.add_exception_handler(NotAuth, not_auth_handler)
    app.add_exception_handler(PositionNonExists, position_non_exists_handler)


def __exc_response(status_code: int, detail) -> Response:
    return JSONResponse(
        status_code=status_code,
        content={
            "detail": detail,
        }
    )


async def bad_request_handler(_, exc: BadRequest):
    return __exc_response(400, exc.message)


async def not_found_handler(_, exc: NotFound):
    return __exc_response(404, exc.message)


async def not_auth_handler(_, exc: NotAuth):
    return __exc_response(403, exc.message)


async def position_non_exists_handler(_, exc: PositionNonExists):
    return __exc_response(
        400,
        {"not_found_positions": exc.shift_task_positions},
    )


__all__ = ["add_exc_handlers"]
