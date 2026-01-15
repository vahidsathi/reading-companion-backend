from sqlalchemy import Integer, Text, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Passage(Base):
    __tablename__ = "passages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    grade: Mapped[int] = mapped_column(Integer, index=True)  # 1..5
    passage_code: Mapped[str | None] = mapped_column(String(20), unique=True, index=True, nullable=True)
    title: Mapped[str] = mapped_column(String(200), default="")
    text: Mapped[str] = mapped_column(Text)
