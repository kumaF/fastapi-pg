from typing import Any

from cachetools import TTLCache


_cache = TTLCache(maxsize=1024, ttl=15)


def set_cache(key: str, value: Any) -> None:  # noqa: ANN401
    """Store a value in the cache under the specified key.

    Args:
        key: The cache key used to store the value.
        value: The value to be stored in the cache.

    Returns:
        None.
    """
    _cache[key] = value


def read_cache(key: str) -> Any:  # noqa: ANN401
    """Retrieve a value from the cache by its key.

    Args:
        key: The cache key to look up in the cache.

    Returns:
        The cached value associated with the given key if it exists;
        otherwise, None.
    """
    if key not in _cache:
        return None

    return _cache[key]


__all__ = [
    'set_cache',
    'read_cache',
]
