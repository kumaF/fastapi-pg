from datetime import datetime

import ulid

from sqlalchemy import (
    func,
    text,
)
from sqlalchemy.dialects.postgresql import (
    ARRAY,
    BOOLEAN,
    CHAR,
    TEXT,
    TIMESTAMP,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import Base


class ServiceApiKeyModel(Base):
    __tablename__ = 'service_api_keys'
    __table_args__ = {'schema': 'core'}

    id: Mapped[str] = mapped_column(
        type_=CHAR(26),
        primary_key=True,
        nullable=False,
        unique=True,
        index=True,
        default=lambda: ulid.new().str,
    )

    service_name: Mapped[str] = mapped_column(
        type_=TEXT,
        nullable=False,
        unique=True,
    )

    key_hash: Mapped[str] = mapped_column(
        type_=TEXT,
        nullable=False,
        unique=True,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        type_=BOOLEAN,
        nullable=False,
        server_default=text('true'),
    )

    scopes: Mapped[list[str]] = mapped_column(
        type_=ARRAY(TEXT),
        nullable=False,
        server_default=text("'{}'::text[]"),
    )

    last_used_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        server_onupdate=func.now(),
    )
