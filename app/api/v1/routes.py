from fastapi import APIRouter

from app.api.v1.endpoints import (
    apikey_router,
    auth_router,
    freshness_router,
    health_router,
    meta_router,
    price_router,
)


router = APIRouter()
api_version_prefix: str = '/v1'

router.include_router(health_router, prefix=api_version_prefix)
router.include_router(auth_router, prefix=api_version_prefix)
router.include_router(apikey_router, prefix=api_version_prefix)
router.include_router(price_router, prefix=api_version_prefix)
router.include_router(meta_router, prefix=api_version_prefix)
router.include_router(freshness_router, prefix=api_version_prefix)
