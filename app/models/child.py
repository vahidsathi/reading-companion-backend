from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Child(Base):
    __tablename__ = "children"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    display_name: Mapped[str] = mapped_column(String(80))
    grade: Mapped[int] = mapped_column(Integer, index=True)  # 1..5
