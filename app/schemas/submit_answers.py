from pydantic import BaseModel, Field

class AnswerIn(BaseModel):
    question_id: int
    selected_choice: str = Field(pattern="^[ABCD]$")

class SubmitAnswersIn(BaseModel):
    child_id: int
    passage_id: int
    answers: list[AnswerIn]
