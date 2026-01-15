from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.child import Child
from app.models.passage import Passage
from app.models.progress import ChildPassageHistory
from app.models.question import Question


class NoPassagesAvailable(Exception):
    pass


MIN_QUESTIONS = 2  # change to 3 later if you want


def get_next_passage_for_child(db: Session, child_id: int) -> Passage:
    child = db.get(Child, child_id)
    if not child:
        raise ValueError("Child not found")

    used_ids_subq = (
        select(ChildPassageHistory.passage_id)
        .where(ChildPassageHistory.child_id == child_id)
        .subquery()
    )

    # Pick an unused passage that has at least MIN_QUESTIONS questions
    stmt = (
        select(Passage)
        .join(Question, Question.passage_id == Passage.id)
        .where(Passage.grade == child.grade)
        .where(Passage.id.not_in(select(used_ids_subq.c.passage_id)))
        .group_by(Passage.id)
        .having(func.count(Question.id) >= MIN_QUESTIONS)
        .order_by(func.random())
        .limit(1)
    )

    passage = db.execute(stmt).scalars().first()

    # If all eligible passages were used, recycle among eligible passages
    if not passage:
        passage = db.execute(
            select(Passage)
            .join(Question, Question.passage_id == Passage.id)
            .where(Passage.grade == child.grade)
            .group_by(Passage.id)
            .having(func.count(Question.id) >= MIN_QUESTIONS)
            .order_by(func.random())
            .limit(1)
        ).scalars().first()

    if not passage:
        raise NoPassagesAvailable(
            f"No passages exist for this grade with at least {MIN_QUESTIONS} questions"
        )

    # record assignment (only first time)
    existing = db.execute(
        select(ChildPassageHistory)
        .where(ChildPassageHistory.child_id == child_id)
        .where(ChildPassageHistory.passage_id == passage.id)
        .limit(1)
    ).scalars().first()

    if not existing:
        db.add(ChildPassageHistory(child_id=child_id, passage_id=passage.id, status="assigned"))
        db.commit()

    return passage
