from typing import Annotated

from fastapi import (
    Depends,
    Request,
)
from sqlalchemy import text
from sqlalchemy.exc import (
    DataError,
    IntegrityError,
    OperationalError,
    SQLAlchemyError,
)
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_CONTENT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.core.cache import read_cache
from app.db.session import get_session
from app.schemas.error import DetailedError


async def get_db_response_time_ms(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> str:
    """Measure and return the database response time for the current request.

    This function executes a lightweight database query to ensure an active
    connection and then retrieves the database response duration from the
    request-scoped cache using the request ID. If a duration is found, it is
    converted from nanoseconds to milliseconds and formatted as a string.

    Args:
        request: The incoming HTTP request containing request-scoped state.
        session: An active asynchronous database session provided as a
            dependency.

    Returns:
        A formatted string representing the database response time in
        milliseconds if available; otherwise, None.
    """
    r = await session.execute(text('SELECT 1'))
    r.one_or_none()
    duration_ns = read_cache(request.state.request_id)

    if duration_ns is not None:
        duration_ms: float = duration_ns / 1_000_000
        return f'{duration_ms:.2} ms'

    return duration_ns


async def handle_db_errors(e: SQLAlchemyError) -> DetailedError:
    if isinstance(e, DataError):
        return DetailedError(
            status_code=HTTP_422_UNPROCESSABLE_CONTENT,
            message='Incorrect data.',
            errors=[{'code': e.code, 'details': e._message()}]
        )
    
    if isinstance(e, IntegrityError):
        return DetailedError(
            status_code=HTTP_409_CONFLICT,
            message='Duplicate entry',
            errors=[{'code': e.code, 'details': e._message()}]
        )
    if isinstance(e, OperationalError):
        return DetailedError(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            message='Query failed due to lock/dead lock issues.',
            errors=[{'code': e.code, 'details': e._message()}]
        )
    
    return DetailedError(
        status_code=HTTP_400_BAD_REQUEST,
        message='Unexpected SQLAlchemy error.',
        errors=[{'code': e.code, 'details': e._message()}]
    )