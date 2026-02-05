from fastapi import FastAPI

from app.api import v1_router
from app.core.lifespan import lifespan
from app.core.middlewares import AddRequestIdMiddleware


api_prefix: str = '/api'
app = FastAPI(lifespan=lifespan)

app.add_middleware(AddRequestIdMiddleware)

app.include_router(v1_router, prefix=api_prefix)
