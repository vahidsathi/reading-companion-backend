from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
import json
from pathlib import Path

from app.api.deps import get_db
from app.models.passage import Passage
from app.models.question import Question

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/import_grade/{grade}")
def import_grade(grade: int, db: Session = Depends(get_db)):
    if grade < 1 or grade > 5:
        raise HTTPException(status_code=400, detail="grade must be 1..5")

    root = Path(".").resolve()
    p_path = root / "data" / "passages" / f"grade{grade}.json"
    q_path = root / "data" / "questions" / f"grade{grade}_questions.json"

    if not p_path.exists() or not q_path.exists():
        raise HTTPException(status_code=404, detail=f"Missing data files for grade {grade}")

    passages = json.loads(p_path.read_text(encoding="utf-8"))
    questions = json.loads(q_path.read_text(encoding="utf-8"))

    if isinstance(passages, dict):
        passages = passages.get("passages") or passages.get("items") or passages.get("data") or []
    if isinstance(questions, dict):
        questions = questions.get("questions") or questions.get("items") or questions.get("data") or []

    # Build passage_code -> Passage row
    inserted_passages = 0
    inserted_questions = 0

    # preload existing passage_codes to avoid duplicates
    existing = set(db.execute(select(Passage.passage_code)).scalars().all())

    code_to_id = {}

    for p in passages:
        code = p.get("passage_code")
        if not code:
            continue
        if code in existing:
            # fetch id
            pid = db.execute(select(Passage.id).where(Passage.passage_code == code)).scalar_one()
            code_to_id[code] = pid
            continue

        row = Passage(
            grade=int(p.get("grade", grade)),
            passage_code=code,
            title=p.get("title", "") or "",
            text=p.get("text", "") or "",
        )
        db.add(row)
        db.flush()  # get row.id
        code_to_id[code] = row.id
        inserted_passages += 1

    # insert questions
    for q in questions:
        code = q.get("passage_code")
        if not code:
            continue
        pid = code_to_id.get(code)
        if not pid:
            continue

        # avoid duplicating questions if you re-run import
        # (simple check: same prompt + passage_id)
        prompt = (q.get("prompt") or "").strip()
        if not prompt:
            continue

        exists = db.execute(
            select(Question.id)
            .where(Question.passage_id == pid)
            .where(Question.prompt == prompt)
        ).first()
        if exists:
            continue

        row = Question(
            passage_id=pid,
            prompt=prompt,
            choice_a=q.get("choice_a", "") or "",
            choice_b=q.get("choice_b", "") or "",
            choice_c=q.get("choice_c", "") or "",
            choice_d=q.get("choice_d", "") or "",
            correct_choice=(q.get("correct_choice", "") or "A").strip()[:1],
        )
        db.add(row)
        inserted_questions += 1

    db.commit()

    return {
        "grade": grade,
        "inserted_passages": inserted_passages,
        "inserted_questions": inserted_questions,
        "total_passages_seen": len(passages),
        "total_questions_seen": len(questions),
    }
