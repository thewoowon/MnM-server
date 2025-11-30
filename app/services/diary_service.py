from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import date, datetime
from app.models.diary import Diary
from app.models.user import User
from app.schemas.diary import DiaryCreate, DiaryResponse
from typing import List, Optional


def create_diary(db: Session, user_id: int, diary_data: DiaryCreate) -> Diary:
    """일기 생성"""
    # 유저 존재 확인
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 오늘 날짜로 이미 일기가 있는지 확인
    diary_date = diary_data.diary_date or date.today()
    existing_diary = db.query(Diary).filter(
        and_(
            Diary.user_id == user_id,
            Diary.diary_date == diary_date
        )
    ).first()

    if existing_diary:
        raise HTTPException(
            status_code=400,
            detail=f"Diary already exists for {diary_date}"
        )

    # 새 일기 생성
    new_diary = Diary(
        user_id=user_id,
        content=diary_data.content,
        purpose=diary_data.purpose,
        mood=diary_data.mood,
        diary_date=diary_date
    )

    db.add(new_diary)
    db.commit()
    db.refresh(new_diary)

    return new_diary


def get_user_diaries(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Diary]:
    """유저의 모든 일기 조회 (최신순)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    diaries = db.query(Diary).filter(Diary.user_id == user_id)\
        .order_by(Diary.diary_date.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()

    return diaries


def get_diary_by_date(db: Session, user_id: int, diary_date: date) -> Optional[Diary]:
    """특정 날짜의 일기 조회"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    diary = db.query(Diary).filter(
        and_(
            Diary.user_id == user_id,
            Diary.diary_date == diary_date
        )
    ).first()

    if not diary:
        raise HTTPException(
            status_code=404,
            detail=f"Diary not found for {diary_date}"
        )

    return diary


def get_today_diary(db: Session, user_id: int) -> Optional[Diary]:
    """오늘 작성한 일기 조회"""
    return get_diary_by_date(db, user_id, date.today())
