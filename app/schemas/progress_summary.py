from pydantic import BaseModel
from datetime import datetime

class ProgressSummaryOut(BaseModel):
    child_id: int
    total_assigned: int
    total_completed: int
    completion_rate: float
    avg_score: float | None
    last_completed_at: datetime | None
