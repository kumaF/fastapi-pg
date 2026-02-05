from time import perf_counter_ns

from fastapi import Request
from psutil import (
    cpu_percent,
    virtual_memory,
)

from app.schemas.core import SystemMetrics


def get_api_uptime(request: Request) -> str:
    """Return the API uptime as a human-readable string.

    Calculates the elapsed time since the application start using a
    high-resolution performance counter. If the start time is not
    available in the application state, returns "n/a".

    Args:
        request: The incoming FastAPI request object. The application
            state may contain `start_time_ns`, representing the API
            start time in nanoseconds.

    Returns:
        A string representing the API uptime in the format:
        "{days} days, {hours} hours, {minutes} minutes, {seconds} seconds",
        or "n/a" if the start time is unavailable.
    """
    start_time_ns = getattr(request.app.state, 'start_time_ns', None)

    if not start_time_ns:
        return 'n/a'

    elapsed_ns = perf_counter_ns() - start_time_ns
    elapsed_seconds = elapsed_ns / 1_000_000_000

    # Calculate days, hours, minutes, and seconds
    days = int(elapsed_seconds // 86400)  # 86400 seconds in a day
    hours = int((elapsed_seconds % 86400) // 3600)  # 3600 seconds in an hour
    minutes = int((elapsed_seconds % 3600) // 60)  # 60 seconds in a minute
    seconds = int(elapsed_seconds % 60)  # Remaining seconds

    return f'{days} days, {hours} hours, {minutes} minutes, {seconds} seconds'


def get_system_metrics() -> SystemMetrics:
    """Retrieve current system CPU and memory usage metrics.

    Returns:
        dict: A dictionary containing system usage metrics with percentage
        values as strings.
            - cpu_usage (str): CPU usage percentage (e.g., "42%").
            - memory_usage (str): Memory usage percentage (e.g., "73%").
    """
    return {
        'cpu_usage': f'{cpu_percent()}%',
        'memory_usage': f'{virtual_memory().percent}%',
    }
