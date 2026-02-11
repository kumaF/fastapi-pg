from typing import (
    TYPE_CHECKING,
    Annotated,
)

from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.responses import JSONResponse

from app.services.apikey import create_api_key


if TYPE_CHECKING:
    from app.schemas.response import ResponseModel

router = APIRouter(prefix='/apikeys')


@router.post('')
async def check_health(
    result: Annotated['ResponseModel', Depends(create_api_key)],
) -> JSONResponse:
    return JSONResponse(
        status_code=result.status,
        content=result.model_dump(exclude_none=True),
    )
