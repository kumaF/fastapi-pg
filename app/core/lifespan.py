from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from time import perf_counter_ns

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application startup and shutdown lifecycle state.

    This lifespan function records the application start time in nanoseconds
    and stores it on the FastAPI application state during startup. The value
    is removed during application shutdown.

    Args:
        app: The FastAPI application instance.

    Yields:
        None
    """
    start_time_ns: int = perf_counter_ns()
    app.state.start_time_ns = start_time_ns

    yield

    del app.state.start_time_ns
