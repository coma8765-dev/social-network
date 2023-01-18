import logging
import random
import string
import time
import sys

from fastapi import Response, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse

logger = logging.getLogger("app.access")


async def logging_middleware(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request {request.method.lower()} {request.url.path}")
    start_time = time.time()

    response = None
    try:
        response = await call_next(request)
    except:
        raise
    finally:
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        logger.info(f"rid={idem} time {formatted_process_time}ms "
                    f"status_code={response and response.status_code or 500}")

    return response


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self,
            rq: Request,
            handler: RequestResponseEndpoint,
    ) -> Response:
        # noinspection PyBroadException
        try:
            return await handler(rq)
        except Exception as e:
            # noinspection PyBroadException
            # try:
            #     data = rq.method == "POST" and rq.headers["content-type"] == "application/json" and rq._json
            # except:
            data = None

            exc_type, exc_obj, exc_tb = sys.exc_info()

            logger.exception(
                msg={
                    "url": rq.url.path,
                    "query_params": rq.query_params,
                    "path_params": rq.path_params,
                    "post": data,
                    "exc": {
                        "type": exc_type,
                        "obj": exc_obj,
                        "traceback": {
                            "path": exc_tb.tb_frame.f_code.co_filename,
                            "line": exc_tb.tb_lineno,
                        },
                    },
                },
                exc_info=True
            )

            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal Server Error",
                }
            )
