from datetime import datetime

import ulid

from sqlalchemy import (
    ForeignKey,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import (
    BOOLEAN,
    CHAR,
    TEXT,
    TIMESTAMP,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import Base


class UserModel(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': None}

    id: Mapped[str] = mapped_column(
        type_=CHAR(26),
        primary_key=True,
        nullable=False,
        unique=True,
        index=True,
        default=lambda: ulid.new().str,
    )

    username: Mapped[str] = mapped_column(
        type_=TEXT,
        nullable=False,
        unique=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        type_=TEXT,
        nullable=False,
        unique=True,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        type_=TEXT,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        type_=BOOLEAN,
        nullable=False,
        server_default=text('false'),
    )

    is_verified: Mapped[bool] = mapped_column(
        type_=BOOLEAN,
        nullable=False,
        server_default=text('false'),
    )

    is_deleted: Mapped[bool] = mapped_column(
        type_=BOOLEAN,
        nullable=False,
        server_default=text('false'),
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

    # relationships

    user_profile: Mapped['UserProfileModel'] = relationship(
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan',
    )


class UserProfileModel(Base):
    __tablename__ = 'user_profiles'
    __table_args__ = {'schema': None}

    id: Mapped[str] = mapped_column(
        type_=CHAR(26),
        primary_key=True,
        nullable=False,
        unique=True,
        index=True,
        default=lambda: ulid.new().str,
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        unique=True,
    )

    first_name: Mapped[str | None] = mapped_column(
        type_=TEXT,
        nullable=True,
    )

    last_name: Mapped[str | None] = mapped_column(
        type_=TEXT,
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

    # relationships

    user: Mapped['UserModel'] = relationship(
        back_populates='user_profile',
    )