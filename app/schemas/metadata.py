from app.schemas.base import BaseSchema


class MetadataSchema(BaseSchema):
    id: int
    value: str