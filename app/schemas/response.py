import datetime as dt

from datetime import datetime
from typing import (
    # TYPE_CHECKING,
    Self,
)

from pydantic import (
    BaseModel,
    Field,
)
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from app.core.request import get_request_id


# if TYPE_CHECKING:
# from fastapi.requests import Request


class ResponseModel(BaseModel):
    """Standard API response model.

    This model provides a consistent structure for API responses, including
    status information, payload data, optional messages, and error details.
    A timestamp is automatically generated at creation time.

    Attributes:
        status (int): HTTP status code of the response.
        success (bool): Indicates whether the request was successful. Automatically derived from the status code.
        payload (dict | list | None): Response data payload.
        message (str | None): Optional human-readable message.
        errors (list | None): Optional list of error details.
        timestamp (str): ISO 8601 timestamp indicating when the response was generated.
    """

    status: int
    success: bool
    payload: dict | list | None = Field(default=None)
    message: str | None = Field(default=None)
    errors: list | None = Field(default=None)
    next_cursor: str | None = Field(default=None),
    # pagination: ResponsePaginationModel | dict | None = Field(default=None)
    # links: ResponseLinkModel | dict | None = Field(default=None)
    # meta: ResponseMetaModel | dict | None = Field(default=None)
    request_id: str = Field(default_factory=get_request_id)
    timestamp: str = Field(default_factory=lambda: datetime.now(dt.UTC).isoformat())

    @classmethod
    def create_model(
        cls,
        *,
        # request: Request,
        # query_params: QueryParams,
        status: int = HTTP_200_OK,
        payload: dict | list | None = None,
        message: str | None = None,
        errors: list | None = None,
        next_cursor: str | None = None,
        # result_count: int = 0,
    ) -> Self:
        """Create a standardized response model instance.

        This factory method determines the success flag based on the provided
        HTTP status code and returns a populated ResponseModel instance.

        Args:
            status (int, optional): HTTP status code for the response. Defaults to HTTP_200_OK.
            payload (dict | list | None, optional): Response data. Defaults to None.
            message (str | None, optional): Optional message describing the response. Defaults to None.
            errors (list | None, optional): Optional list of errors associated with the response. Defaults to None.

        Returns:
            ResponseModel: A fully constructed response model instance.
        """
        # pagination_model = ResponsePaginationModel(
        #     total_items=result_count,
        #     current_page=query_params.page,
        #     per_page=result_count if query_params.per_page is None else query_params.per_page
        # )

        # links_model = ResponseLinkModel(
        #     pagination=pagination_model,
        #     url=str(request.url)
        # )

        # meta_model = ResponseMetaModel(
        #     sort_by=query_params.sort_by,
        #     sort_order=query_params.sort_order,
        #     filters=query_params.model_dump(
        #         mode='json',
        #         exclude=[
        #             'sort_by',
        #             'sort_order',
        #             'page',
        #             'per_page'
        #         ],
        #         exclude_none=True
        #     )
        # )

        success: bool = status >= HTTP_200_OK and status < HTTP_400_BAD_REQUEST

        return cls(
            status=status,
            success=success,
            payload=payload,
            message=message,
            errors=errors,
            next_cursor=next_cursor,
            # pagination=pagination_model,
            # links=links_model,
            # meta=meta_model
        )


__all__ = ['ResponseModel']
