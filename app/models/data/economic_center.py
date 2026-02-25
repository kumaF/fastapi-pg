
from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import (
    CHAR,
    SMALLINT,
    TEXT,
    TIMESTAMP,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import Base


class EconomicCenterModel(Base):
    __tablename__ = 'dim_economic_center'
    __table_args__ = {'schema': 'crop_price_dw'}

    id: Mapped[int] = mapped_column(
        type_=SMALLINT,
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        type_=TEXT,
        nullable=False,
        unique=True,
    )

    description: Mapped[str] = mapped_column(
        type_=TEXT,
        nullable=True,
        unique=False,
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

    translations: Mapped[list['EconomicCenterTranslationModel']] = relationship(
        back_populates='economic_center',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )



class EconomicCenterTranslationModel(Base):
    __tablename__ = 'economic_center_translation'
    __table_args__ = {'schema': 'crop_price_dw'}

    ref_id: Mapped[int] = mapped_column(
        ForeignKey('crop_price_dw.dim_economic_center.id', ondelete='CASCADE'),
        type_=SMALLINT,
        primary_key=True,
    )

    language_code: Mapped[str] = mapped_column(
        type_=CHAR(2),
        primary_key=True,

    )
    name: Mapped[str] = mapped_column(
        type_=TEXT,
        nullable=False,
        unique=True,
    )

    description: Mapped[str] = mapped_column(
        type_=TEXT,
        nullable=True,
        unique=False,
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

    economic_center: Mapped['EconomicCenterModel'] = relationship(
        back_populates='translations'
    )