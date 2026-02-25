from datetime import datetime

from sqlalchemy.dialects.postgresql import (
    TEXT,
    TIMESTAMP,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.models.base import Base


class MVDataFreshnessModel(Base):    
    __tablename__ = 'mv_data_freshness'
    __table_args__ = {'schema': 'manifests'}

    data_source: Mapped[str] = mapped_column(
        type_=TEXT,
        primary_key=True
    )

    processed_at: Mapped[datetime] = mapped_column(
        type_=TIMESTAMP(timezone=True),
        nullable=False
    )
