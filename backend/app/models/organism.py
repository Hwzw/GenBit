from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Organism(Base):
    __tablename__ = "organisms"

    tax_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scientific_name: Mapped[str] = mapped_column(String(255))
    common_name: Mapped[str | None] = mapped_column(String(255))
    lineage: Mapped[str | None] = mapped_column(Text)
    gc_content: Mapped[float | None] = mapped_column(Float)
    last_fetched: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
