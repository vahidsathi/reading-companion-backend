from sqlalchemy import Integer, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    passage_id: Mapped[int] = mapped_column(ForeignKey("passages.id", ondelete="CASCADE"), index=True)

    prompt: Mapped[str] = mapped_column(Text)
    choice_a: Mapped[str] = mapped_column(String(200))
    choice_b: Mapped[str] = mapped_column(String(200))
    choice_c: Mapped[str] = mapped_column(String(200))
    choice_d: Mapped[str] = mapped_column(String(200), default="")
    correct_choice: Mapped[str] = mapped_column(String(1))  # "A","B","C","D"
