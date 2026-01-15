from sqlalchemy import select

from app.schemas.submit_answers import SubmitAnswersIn
from app.services.scoring_service import score_answers

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.progress import CompleteLessonIn
from app.services.progress_service import complete_lesson

from app.schemas.progress_summary import ProgressSummaryOut
from app.services.progress_summary_service import get_progress_summary

from app.services.progress_service import reset_progress

from app.models.question import Question


router = APIRouter(prefix="/progress", tags=["progress"])

@router.post("/submit")
def submit(payload: SubmitAnswersIn, db: Session = Depends(get_db)):
    # Guard: must submit answers for ALL questions in this passage,
    # and all submitted question_ids must belong to this passage.
    submitted_ids = {a.question_id for a in payload.answers}

    expected_ids = set(
        db.execute(
            select(Question.id).where(Question.passage_id == payload.passage_id)
        ).scalars().all()
    )

    if not expected_ids:
        raise HTTPException(status_code=400, detail="Passage has no questions.")

    if submitted_ids != expected_ids:
        raise HTTPException(
            status_code=400,
            detail="Must submit answers for all questions in this lesson (and only those questions).",
        )

    # 1) compute score
    correct, total = score_answers(db, payload.answers)
    score = int(round((correct / total) * 100)) if total else 0

    # 2) mark completed + store score (allows resubmission; later summary uses BEST attempt)
    complete_lesson(db, payload.child_id, payload.passage_id, score)

    # 3) return result to Android
    return {
        "status": "ok",
        "correct": correct,
        "total": total,
        "score": score
    }

    
@router.get("/summary", response_model=ProgressSummaryOut)
def summary(child_id: int, db: Session = Depends(get_db)):
    data = get_progress_summary(db, child_id)
    return ProgressSummaryOut(**data)

@router.post("/reset")
def reset(child_id: int, db=Depends(get_db)):
    reset_progress(db, child_id)
    return {"status": "ok"}


