from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate


def create_user(db: Session, user: UserCreate):
    db_user = User(
        name=user.name,
        email=user.email,
        profile_pic=user.profile_pic,
        provider=user.provider,
        provider_id=user.provider_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
