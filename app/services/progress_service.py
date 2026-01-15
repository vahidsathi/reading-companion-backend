from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.progress import ChildPassageHistory

def complete_lesson(db: Session, child_id: int, passage_id: int, score: int) -> None:
    row = db.execute(
        select(ChildPassageHistory)
        .where(ChildPassageHistory.child_id == child_id)
        .where(ChildPassageHistory.passage_id == passage_id)
        .limit(1)
    ).scalars().first()

    if not row:
        # If somehow completed without being assigned, create it.
        row = ChildPassageHistory(child_id=child_id, passage_id=passage_id, status="assigned")
        db.add(row)

    row.status = "completed"
    row.completed_at = __import__("datetime").datetime.utcnow()
    # optional: store score later in table (we can add a column next)
    row.score = score
    db.commit()

from sqlalchemy import delete
from app.models.progress import ChildPassageHistory

def reset_progress(db, child_id: int):
    db.execute(
        delete(ChildPassageHistory).where(ChildPassageHistory.child_id == child_id)
    )
    db.commit()

