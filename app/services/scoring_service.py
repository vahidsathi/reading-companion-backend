from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.question import Question

def score_answers(db: Session, answers) -> tuple[int, int]:
    if not answers:
        return (0, 0)

    qids = [a.question_id for a in answers]
    rows = db.execute(select(Question).where(Question.id.in_(qids))).scalars().all()
    correct_map = {q.id: q.correct_choice for q in rows}

    correct = 0
    total = len(answers)
    for a in answers:
        if correct_map.get(a.question_id) == a.selected_choice:
            correct += 1

    return (correct, total)
