from datetime import date
from typing import (
    TYPE_CHECKING,
    Annotated,
)

from fastapi import (
    Depends,
    Query,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from app.configs.core import settings
from app.core.security import (
    decode_cursor,
    encode_cursor,
)
from app.db.session import get_session
from app.db.utils import handle_db_errors
from app.errors.domain import CursorError
from app.errors.http import HttpDbException
from app.repositories.price_data import PriceDataRepository
from app.schemas.price_data import (
    PastWeekPriceDataResponse,
    PriceCard,
)
from app.schemas.request import (
    LatestCropPriceRequestSchema,
    PastWeekCropPriceRequestSchema,
)
from app.schemas.response import ResponseModel
from app.services.auth import validate_apikey


if TYPE_CHECKING:
    from app.models.data.price_data import (
        MVLatestPriceDataModel,
        MVPastWeekPriceDataModel,
    )


async def fetch_latest_crop_price_data(
    session: Annotated[AsyncSession, Depends(get_session)],
    apikey_returns: Annotated[str, Depends(validate_apikey)],
    request_payload: LatestCropPriceRequestSchema,
    cursor: Annotated[str | None, Query] = None,
    limit: Annotated[int, Query] = 10,
) -> ResponseModel:
    _ = apikey_returns
    
    repo = PriceDataRepository(session)

    next_cursor: str | None = None
    cursor_id: int | None = None

    if cursor:
        _, cursor_id = decode_cursor(cursor)

    try:
        async with session.begin():
            price_data: list[MVLatestPriceDataModel] = await repo.find_latest_price_data(
                lang_code=request_payload.language_code,
                economic_center_id=request_payload.economic_center_id,
                crop_ids=request_payload.crop_ids,
                category_ids=request_payload.category_ids,
                cursor_id=cursor_id,
                limit=limit,
            )

            if price_data and len(price_data) == limit:
                last_record = price_data[-1]
                next_cursor = encode_cursor(
                    cursor_id=last_record.id,
                    expires_in_seconds=settings.cursor_exp_delta,
                )

            return ResponseModel.create_model(
                status=HTTP_200_OK,
                payload=[
                    PriceCard.create_model(
                        item=item
                    ).model_dump() for item in price_data
                ],
                next_cursor=next_cursor
            )
    except SQLAlchemyError as e:
        err = await handle_db_errors(e)
        raise HttpDbException(
            status_code=err.status_code,
            message=err.message,
            errors=err.errors
        ) from e
    except CursorError as e:
        raise HttpDbException(
            status_code=HTTP_400_BAD_REQUEST,
            message=f'{e.message}'
        ) from e
    

async def fetch_past_week_price_data(
    session: Annotated[AsyncSession, Depends(get_session)],
    apikey_returns: Annotated[str, Depends(validate_apikey)],
    request_payload: PastWeekCropPriceRequestSchema,
    cursor: Annotated[str | None, Query] = None,
    limit: Annotated[int, Query] = 10,
) -> ResponseModel:
    _ = apikey_returns
    
    repo = PriceDataRepository(session)

    next_cursor: str | None = None
    cursor_date: date | None = None

    try:
        if cursor:
            cursor_date, _ = decode_cursor(cursor)

        async with session.begin():
            price_data: list[MVPastWeekPriceDataModel] = await repo.find_past_week_price_data(
                economic_center_id=request_payload.economic_center_id,
                crop_id=request_payload.crop_id,
                cursor_date=cursor_date,
                limit=limit,
            )

            if price_data and len(price_data) == limit:
                last_record = price_data[-1]
                next_cursor = encode_cursor(
                    cursor_date=last_record.date,
                    expires_in_seconds=settings.cursor_exp_delta,
                )

            return ResponseModel.create_model(
                status=HTTP_200_OK,
                payload=[
                    PastWeekPriceDataResponse.model_validate(
                        p.to_dict()
                    ).model_dump(mode='json') for p in price_data
                ],
                next_cursor=next_cursor
            )
    except SQLAlchemyError as e:
        err = await handle_db_errors(e)
        raise HttpDbException(
            status_code=err.status_code,
            message=err.message,
            errors=err.errors
        ) from e
    except CursorError as e:
        raise HttpDbException(
            status_code=HTTP_400_BAD_REQUEST,
            message=f'{e.message}'
        ) from e