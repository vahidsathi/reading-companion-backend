from fastapi import FastAPI
from app.core.config import APP_NAME, API_PREFIX

from app.api.lessons import router as lessons_router
from app.api.progress import router as progress_router
from app.api.children import router as children_router

# --- DB init (creates tables if missing) ---
from app.db.session import engine
from app.db.base import Base
from app.models import child  # ensure model is registered with Base metadata

app = FastAPI(title=APP_NAME)

@app.on_event("startup")
def _create_tables():
    Base.metadata.create_all(bind=engine)
# ------------------------------------------

app.include_router(lessons_router, prefix=API_PREFIX)
app.include_router(progress_router, prefix=API_PREFIX)
app.include_router(children_router, prefix=API_PREFIX)

@app.get("/health")
def health():
    return {"status": "ok", "build": "debug-data-endpoint-1"}
import os
from pathlib import Path

@app.get("/debug/data")
def debug_data():
    root = Path(".").resolve()
    passages = (root / "data" / "passages")
    questions = (root / "data" / "questions")
    return {
        "cwd": str(root),
        "passages_exists": passages.exists(),
        "questions_exists": questions.exists(),
        "passages_files": sorted([p.name for p in passages.glob("**/*") if p.is_file()])[:20],
        "questions_files": sorted([p.name for p in questions.glob("**/*") if p.is_file()])[:20],
    }
import json
from pathlib import Path
from fastapi import HTTPException

@app.get("/debug/grade/{grade}")
def debug_grade(grade: int):
    root = Path(".").resolve()
    p_path = root / "data" / "passages" / f"grade{grade}.json"
    q_path = root / "data" / "questions" / f"grade{grade}_questions.json"

    if not p_path.exists():
        raise HTTPException(status_code=404, detail=f"Missing {p_path}")
    if not q_path.exists():
        raise HTTPException(status_code=404, detail=f"Missing {q_path}")

    passages = json.loads(p_path.read_text(encoding="utf-8"))
    questions = json.loads(q_path.read_text(encoding="utf-8"))

    # handle common shapes: list vs dict wrappers
    if isinstance(passages, dict):
        passages_list = passages.get("passages") or passages.get("items") or passages.get("data") or []
    else:
        passages_list = passages

    if isinstance(questions, dict):
        questions_list = questions.get("questions") or questions.get("items") or questions.get("data") or []
    else:
        questions_list = questions

    # attempt to group questions by passage_code or passage_id (best-effort)
    by_key = {}
    for q in questions_list:
        if not isinstance(q, dict):
            continue
        key = q.get("passage_id") or q.get("passage_code") or q.get("passage") or q.get("code")
        by_key.setdefault(str(key), 0)
        by_key[str(key)] += 1

    sample_passage = passages_list[0] if passages_list else None
    sample_question = questions_list[0] if questions_list else None

    return {
        "grade": grade,
        "passages_type": type(passages).__name__,
        "questions_type": type(questions).__name__,
        "passages_count": len(passages_list),
        "questions_count": len(questions_list),
        "group_keys_sample": list(by_key.items())[:10],_

    }