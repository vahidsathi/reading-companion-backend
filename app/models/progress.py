from sqlalchemy import Integer, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class ChildPassageHistory(Base):
    __tablename__ = "child_passage_history"
    __table_args__ = (
        UniqueConstraint("child_id", "passage_id", name="uq_child_passage"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    child_id: Mapped[int] = mapped_column(ForeignKey("children.id", ondelete="CASCADE"), index=True)
    passage_id: Mapped[int] = mapped_column(ForeignKey("passages.id", ondelete="CASCADE"), index=True)

    status: Mapped[str] = mapped_column(String(20), default="assigned")  # assigned|completed|skipped
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)

    assigned_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)
