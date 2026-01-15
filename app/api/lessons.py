from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.lesson import LessonOut
from app.schemas.question import QuestionOut
from app.services.lesson_service import get_next_passage_for_child, NoPassagesAvailable
from app.models.child import Child
from app.models.question import Question

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get("/next", response_model=LessonOut)
def next_lesson(child_id: int, db: Session = Depends(get_db)) -> LessonOut:
    try:
        passage = get_next_passage_for_child(db, child_id=child_id)
        child = db.get(Child, child_id)

        questions = db.execute(
            select(Question)
            .where(Question.passage_id == passage.id)
            .order_by(Question.id)
        ).scalars().all()

        return LessonOut(
            child_id=child_id,
            passage_id=passage.id,
            grade=child.grade if child else passage.grade,
            title=passage.title,
            text=passage.text,
            questions=[
                QuestionOut(
                    id=q.id,
                    prompt=q.prompt,
                    choice_a=q.choice_a,
                    choice_b=q.choice_b,
                    choice_c=q.choice_c,
                    choice_d=q.choice_d,
                )
                for q in questions
            ],
        )
    except NoPassagesAvailable as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
