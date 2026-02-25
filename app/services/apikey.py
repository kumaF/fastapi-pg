from typing import (
    TYPE_CHECKING,
    Annotated,
)

from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_200_OK

from app.core.security import hash_key
from app.db.session import get_session
from app.db.utils import handle_db_errors
from app.errors.http import HttpDbException
from app.repositories.apikey import ServiceApiKeyRepository
from app.schemas.apikey import (
    RequestApiKeySchema,
    ResponseApiKeySchema,
)
from app.schemas.response import ResponseModel
from app.services.auth import validate_access_token


if TYPE_CHECKING:
    from app.models.app.apikey import ServiceApiKeyModel


async def create_api_key(
    session: Annotated[AsyncSession, Depends(get_session)],
    token_returns: Annotated[tuple[dict, dict], Depends(validate_access_token)],
    request_payload: RequestApiKeySchema,
) -> ResponseModel:
    _ = token_returns[0]

    repo = ServiceApiKeyRepository(session)

    request_data = RequestApiKeySchema.model_validate(
        request_payload,
        from_attributes=True,
    )

    try:
        async with session.begin():
            db_data: ServiceApiKeyModel = await repo.create({
                'service_name': request_data.service_name,
                'key_hash': hash_key(request_data.api_key)
            })

            return ResponseModel.create_model(
                status=HTTP_200_OK,
                payload=ResponseApiKeySchema(**{
                    'api_key': request_data.api_key,
                    **db_data.to_dict(),
                }).model_dump(
                    mode='json',
                    include=[
                        'service_name',
                        'api_key',
                        'created_at',
                    ]
                ),
            )
    except SQLAlchemyError as e:
        err = await handle_db_errors(e)
        raise HttpDbException(
            status_code=err.status_code,
            message=err.message,
            errors=err.errors
        ) from e
