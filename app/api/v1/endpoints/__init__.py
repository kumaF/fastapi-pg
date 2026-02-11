from app.api.v1.endpoints.apikey import router as apikey_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.health import router as health_router


__all__ = [
    'health_router',
    'auth_router',
    'apikey_router',
]
