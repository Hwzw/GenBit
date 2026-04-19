import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ElementType(enum.StrEnum):
    PROMOTER = "promoter"
    KOZAK = "kozak"
    CDS = "cds"
    STOP_CODON = "stop_codon"
    TERMINATOR = "terminator"
    TAG = "tag"
    UTR = "utr"
    CUSTOM = "custom"


class ConstructElement(Base):
    __tablename__ = "construct_elements"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    construct_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("constructs.id", ondelete="CASCADE")
    )
    element_type: Mapped[ElementType] = mapped_column(Enum(ElementType))
    label: Mapped[str] = mapped_column(String(255))
    sequence: Mapped[str] = mapped_column(Text)
    position: Mapped[int] = mapped_column(Integer)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    construct: Mapped["Construct"] = relationship(back_populates="elements")  # noqa: F821
