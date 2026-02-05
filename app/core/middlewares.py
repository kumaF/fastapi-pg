import logging

from collections.abc import (
    Awaitable,
    Callable,
)
from time import perf_counter_ns
from typing import TYPE_CHECKING
from uuid import uuid4

from fastapi import (
    Request,
    Response,
)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.configs import core_configs
from app.core.request import (
    remove_request_id,
    set_request_id,
)


if TYPE_CHECKING:
    from contextvars import Token


logger = logging.getLogger(core_configs.logger_name)


class AddRequestIdMiddleware(BaseHTTPMiddleware):
    """Middleware that assigns and manages a unique request ID per request.

    This middleware generates a unique request ID for each incoming HTTP
    request, stores it in the request state, and sets it in a context variable
    for use throughout the request lifecycle (e.g., logging and tracing).
    It also measures and logs the total request processing time.

    The request ID is automatically removed from the context after the
    response is generated to prevent context leakage across requests.
    """

    def __init__(  # noqa: D107
        self,
        app: ASGIApp,
    ) -> None:
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Process an incoming HTTP request and attach a request ID.

        Args:
            request: The incoming HTTP request.
            call_next: A callable that forwards the request to the next
                middleware or route handler.

        Returns:
            The HTTP response returned by the downstream application.
        """
        start_time_ns = perf_counter_ns()
        request_id: str = str(uuid4().hex)
        request.state.request_id = request_id
        ctx_token: Token = await set_request_id(request_id)
        logger.info(f'Start processing request: {request_id}')

        response = await call_next(request)

        await remove_request_id(ctx_token)
        duration_ns: int = perf_counter_ns() - start_time_ns
        duration_ms: float = duration_ns / 1_000_000
        logger.info(
            f'Finished processing request: {request_id} in {duration_ms:.4f} milliseconds'
        )

        return response
