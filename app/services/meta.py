from typing import Annotated

from fastapi import (
    Depends,
    Query,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_200_OK

from app.core.types import (
    AttributeType,
    LanguageCode,
    MetaData,
)
from app.db.session import get_session
from app.db.utils import handle_db_errors
from app.errors.http import HttpDbException
from app.repositories import (
    CropCategoryRepository,
    CropRepository,
    DataSourceRepository,
    EconomicCenterRepository,
    PriceTypeRepository,
)
from app.schemas.metadata import MetadataSchema
from app.schemas.response import ResponseModel
from app.services.auth import validate_apikey


async def fetch_meta_data(
    session: Annotated[AsyncSession, Depends(get_session)],
    apikey_returns: Annotated[str, Depends(validate_apikey)],
    attribute: Annotated[AttributeType, Query],
    language: Annotated[LanguageCode, Query],
) -> ResponseModel:
    _ = apikey_returns
    
    repo_map: dict = {
        'crop': CropRepository,
        'crop_category': CropCategoryRepository,
        'data_source': DataSourceRepository,
        'economic_center': EconomicCenterRepository,
        'price_type': PriceTypeRepository,
    }

    repo = repo_map[attribute](session=session)

    try:
        async with session.begin():
            items: list[MetaData] = await repo.find_metadata(lang=language)

            payload = [MetadataSchema(
                id=item[0],
                value=item[1],
            ) for item in items]

            return ResponseModel.create_model(
                status=HTTP_200_OK,
                payload=payload
            )
    except SQLAlchemyError as e:
        err = await handle_db_errors(e)
        raise HttpDbException(
            status_code=err.status_code,
            message=err.message,
            errors=err.errors
        ) from e
    
    
