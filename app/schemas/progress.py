from pydantic import BaseModel, Field

class CompleteLessonIn(BaseModel):
    child_id: int
    passage_id: int
    score: int = Field(ge=0, le=100)
