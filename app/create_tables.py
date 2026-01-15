from app.db.session import engine
from app.db.base import Base

# Import models so SQLAlchemy knows them
from app.models.passage import Passage  # noqa: F401
from app.models.child import Child      # noqa: F401
from app.models.progress import ChildPassageHistory  # noqa: F401

Base.metadata.create_all(bind=engine)
print("tables created")
