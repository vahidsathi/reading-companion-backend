from pydantic import BaseModel, Field

class ChildCreateIn(BaseModel):
    display_name: str = Field(min_length=1, max_length=50)
    grade: int = Field(ge=1, le=5)

class ChildCreateOut(BaseModel):
    id: int
    display_name: str
    grade: int
