import logging

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio.session import AsyncSession

from app.configs import core_configs
from app.core.request import get_request_id
from app.db.base import Session
from app.db.events import event  # noqa: F401


logger = logging.getLogger(core_configs.logger_name)


async def get_session() -> AsyncGenerator[AsyncSession]:
    """Provide an asynchronous database session for a single request lifecycle.

    This function acts as a dependency that yields an `AsyncSession` instance.
    The session is automatically opened when entering the context and closed
    when the request processing is complete. It also logs the initialization
    of the session using the current request ID, if available.

    Yields:
        An active asynchronous database session.

    Raises:
        Exception: Propagates any exception that occurs during session
            initialization or usage.
    """
    try:
        async with Session() as session:
            logger.info(
                f'Initialized database session for request: {get_request_id()}.'
            )
            yield session
    except Exception as e:
        # logger.error(f'Database error: {e}')

        # if isinstance(e, HTTPException):
        #     raise HTTPException(
        #         status_code=e.status_code,
        #         detail=str(e)
        #     )

        # raise HTTPException(
        #     status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        #     detail=str(e)
        # )
        raise e
