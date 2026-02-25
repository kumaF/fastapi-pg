from fastapi.exceptions import HTTPException


class HttpDbException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        errors: list | None = None,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=message
        )

        self.status_code: int = status_code
        self.message: str = message
        self.errors: list = []

        if errors is not None:
            self.errors = errors
        