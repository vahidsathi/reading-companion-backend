import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:Vivi321%@localhost:5432/reading_app"
)

API_PREFIX = "/api"
APP_NAME = "Reading Companion API"
