from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse
from app.services.user_service import get_user_by_id
from app.dependencies import get_db
from app.core.security import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def read(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get current user
    """
    return get_user_by_id(db=db, user_id=user_id)
