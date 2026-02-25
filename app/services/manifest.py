from typing import Annotated

from fastapi import (
    Depends,
    Query,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_200_OK

from app.db.session import get_session
from app.db.utils import handle_db_errors
from app.errors.http import HttpDbException
from app.repositories.manifest import ManifestRepository
from app.schemas.manifest import DataFreshnessResponse
from app.schemas.response import ResponseModel


async def fetch_data_freshness(
    session: Annotated[AsyncSession, Depends(get_session)],
    tz: Annotated[str, Query] = 'UTC',
) -> ResponseModel:
    repo = ManifestRepository(session)

    try:
        async with session.begin():
            source_freshness: dict = await repo.find_data_freshness()
            payload = DataFreshnessResponse.model_validate({
                **source_freshness,
                'tz': tz,
            }).model_dump()

            return ResponseModel.create_model(
                status=HTTP_200_OK,
                payload=payload,
            )
    except SQLAlchemyError as e:
        err = await handle_db_errors(e)
        raise HttpDbException(
            status_code=err.status_code,
            message=err.message,
            errors=err.errors
        ) from e
