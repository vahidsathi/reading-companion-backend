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
    return {"status": "ok"}
