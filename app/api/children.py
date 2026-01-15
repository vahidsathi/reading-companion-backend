from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.child import Child
from app.schemas.child_create import ChildCreateIn, ChildCreateOut

router = APIRouter(prefix="/children", tags=["children"])

@router.post("/create", response_model=ChildCreateOut)
def create_child(payload: ChildCreateIn, db: Session = Depends(get_db)):
    child = Child(display_name=payload.display_name, grade=payload.grade)
    db.add(child)
    db.commit()
    db.refresh(child)
    return ChildCreateOut(id=child.id, display_name=child.display_name, grade=child.grade)
