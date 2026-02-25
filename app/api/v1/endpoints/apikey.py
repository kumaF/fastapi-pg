from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from starlette.status import HTTP_200_OK

from app.schemas.response import ResponseModel
from app.services.apikey import create_api_key
    

router = APIRouter(prefix='/apikeys')


@router.post(
    '',
    status_code=HTTP_200_OK,
    response_model_exclude_none=True,
)
async def check_health(
    result: Annotated['ResponseModel', Depends(create_api_key)],
) -> ResponseModel:
    return result
