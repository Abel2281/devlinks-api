import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Click(Base):
    __tablename__ = "clicks"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    link_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("links.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    ip_address: Mapped[str] = mapped_column(
        String(45), nullable=False
    )
    user_agent: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )
    referrer: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )
    clicked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    link = relationship("Link", back_populates="clicks")