from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from starlette.status import HTTP_200_OK

from app.schemas.response import ResponseModel
from app.services.manifest import fetch_data_freshness
    

router = APIRouter(prefix='/freshness')


@router.get(
    '',
    status_code=HTTP_200_OK,
    response_model_exclude_none=True,
)
def data_freshness(
    result: Annotated['ResponseModel', Depends(fetch_data_freshness)],
) -> ResponseModel:
    return result
