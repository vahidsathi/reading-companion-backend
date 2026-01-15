from pydantic import BaseModel

class QuestionOut(BaseModel):
    id: int
    prompt: str
    choice_a: str
    choice_b: str
    choice_c: str
    choice_d: str
