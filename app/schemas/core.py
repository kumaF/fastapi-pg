from typing import TypedDict


class SystemMetrics(TypedDict):
    """Represents system resource usage metrics.

    Attributes:
        cpu_usage (str): CPU usage percentage (e.g., "42%").
        memory_usage (str): Memory usage percentage (e.g., "73%").
    """

    cpu_usage: str
    memory_usage: str
