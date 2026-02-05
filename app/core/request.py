import logging

from contextvars import (
    ContextVar,
    Token,
)
from typing import Final

from app.configs import core_configs


logger = logging.getLogger(core_configs.logger_name)


REQUEST_ID_CTX_KEY: Final[str] = core_configs.request_id_ctx_key
_request_id_ctx_var: ContextVar[str | None] = ContextVar(
    REQUEST_ID_CTX_KEY, default=None
)


async def set_request_id(request_id: str) -> Token:
    """Set the request ID in the context for the current execution flow.

    This function stores the given request ID in a context variable so it can
    be accessed throughout the lifetime of the request (e.g., for logging or
    tracing). It returns a token that can later be used to reset the context
    variable to its previous state.

    Args:
        request_id: A unique identifier for the current request.

    Returns:
        A context variable token that can be used to restore the previous
        request ID value.
    """
    logger.info(f'Session context initialized for request handling: {request_id}')
    return _request_id_ctx_var.set(request_id)


def get_request_id() -> str | None:
    """Retrieve the current request ID from the context.

    Returns:
        The current request ID if one is set in the context; otherwise, None.
    """
    return _request_id_ctx_var.get()


async def remove_request_id(token: Token) -> None:
    """Remove the request ID from the context and restore the previous value.

    This function resets the context variable using the token returned by
    `set_request_id`, ensuring the context is cleaned up after request
    processing is complete.

    Args:
        token: The context variable token returned by `set_request_id`.

    Returns:
        None.
    """
    _request_id_ctx_var.reset(token)


# def default_fields(default_fields: dict[UserType, list] | list[str]):
#     def decorator(func: Callable):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             query_params: QueryParams = kwargs.get('query_params')
#             fields = default_fields

#             if isinstance(default_fields, dict):
#                 token_returns, _ = kwargs.get('token_returns', None)
#                 identity_type = UserType(token_returns['identity_type'])

#                 fields = default_fields.get(identity_type, None)

#             if not query_params.fields and fields:
#                 query_params.fields = fields
#                 kwargs.update({'query_params': query_params})

#             return await func(*args, **kwargs)
#         return wrapper
#     return decorator
