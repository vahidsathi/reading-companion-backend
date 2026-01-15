import os

API_PREFIX = "/api"
APP_NAME = "Reading Companion API"

_raw_db = os.getenv("DATABASE_URL", "")

# Render often provides DATABASE_URL like: postgres://...
# SQLAlchemy expects: postgresql+psycopg2://...
if _raw_db.startswith("postgres://"):
    _raw_db = _raw_db.replace("postgres://", "postgresql+psycopg2://", 1)

DATABASE_URL = _raw_db or "postgresql+psycopg2://postgres:Vivi321%@localhost:5432/reading_app"
