from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/")
def get_dashboard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return {"message": "Dashboard working", "user": current_user.name}