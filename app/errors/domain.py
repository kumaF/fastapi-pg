from app.schemas.error import DetailedError

class BaseError(Exception):
    def __init__(
        self,
        message: str,
        errors: list | None = None
    ) -> None:
        self.message = message
        self.errors = errors

        super().__init__(message)

class TokenError(BaseError):
    pass