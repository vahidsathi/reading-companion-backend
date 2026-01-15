from pydantic import BaseModel

class LessonOut(BaseModel):
    child_id: int
    passage_id: int
    grade: int
    title: str
    text: str

from pydantic import BaseModel
from app.schemas.question import QuestionOut

class LessonOut(BaseModel):
    child_id: int
    passage_id: int
    grade: int
    title: str
    text: str
    questions: list[QuestionOut]

