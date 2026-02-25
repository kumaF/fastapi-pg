from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from starlette.status import HTTP_200_OK

from app.schemas.response import ResponseModel
from app.services.price import (
    fetch_latest_crop_price_data,
    fetch_past_week_price_data,
)
    

router = APIRouter(prefix='/price-data')


@router.get(
    '/latest',
    status_code=HTTP_200_OK,
    response_model_exclude_none=True,
)
def get_latest_crop_price(
    result: Annotated['ResponseModel', Depends(fetch_latest_crop_price_data)],
) -> ResponseModel:
    return result


@router.get(
    '/history',
    status_code=HTTP_200_OK,
    response_model_exclude_none=True,
)
def get_crop_price_history(
    result: Annotated['ResponseModel', Depends(fetch_past_week_price_data)],
) -> ResponseModel:
    return result