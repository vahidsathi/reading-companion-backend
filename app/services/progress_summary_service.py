from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.progress import ChildPassageHistory


def get_progress_summary(db: Session, child_id: int):
    # total_assigned = distinct passages ever assigned to this child
    total_assigned = db.execute(
        select(func.count(func.distinct(ChildPassageHistory.passage_id)))
        .where(ChildPassageHistory.child_id == child_id)
    ).scalar_one()

    # total_completed = distinct passages completed (at least once)
    total_completed = db.execute(
        select(func.count(func.distinct(ChildPassageHistory.passage_id)))
        .where(ChildPassageHistory.child_id == child_id)
        .where(ChildPassageHistory.status == "completed")
    ).scalar_one()

    # avg_score = average of BEST score per passage (among completed rows)
    best_scores_subq = (
        select(
            ChildPassageHistory.passage_id,
            func.max(ChildPassageHistory.score).label("best_score"),
        )
        .where(ChildPassageHistory.child_id == child_id)
        .where(ChildPassageHistory.status == "completed")
        .where(ChildPassageHistory.score.is_not(None))
        .group_by(ChildPassageHistory.passage_id)
        .subquery()
    )

    avg_score = db.execute(
        select(func.avg(best_scores_subq.c.best_score))
    ).scalar()

    last_completed_at = db.execute(
        select(func.max(ChildPassageHistory.completed_at))
        .where(ChildPassageHistory.child_id == child_id)
        .where(ChildPassageHistory.status == "completed")
    ).scalar()

    completion_rate = (total_completed / total_assigned) if total_assigned else 0.0

    return {
        "child_id": child_id,
        "total_assigned": int(total_assigned),
        "total_completed": int(total_completed),
        "completion_rate": float(completion_rate),
        "avg_score": float(avg_score) if avg_score is not None else None,
        "last_completed_at": last_completed_at,
    }
