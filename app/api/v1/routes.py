from fastapi import APIRouter

from app.api.v1.endpoints import health_router


router = APIRouter()
api_version_prefix: str = '/v1'

router.include_router(health_router, prefix=api_version_prefix)
