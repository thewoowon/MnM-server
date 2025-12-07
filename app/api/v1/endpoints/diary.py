from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from app.dependencies import get_db
from app.core.security import get_current_user
from app.schemas.diary import DiaryCreate, DiaryResponse
from app.services import diary_service

router = APIRouter()


@router.post("/", response_model=DiaryResponse)
def create_diary(
    diary_data: DiaryCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """일기 작성"""
    return diary_service.create_diary(db, current_user_id, diary_data)


@router.get("/", response_model=List[DiaryResponse])
def get_my_diaries(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """내 모든 일기 조회 (최신순)"""
    return diary_service.get_user_diaries(db, current_user_id, skip, limit)


@router.get("/today", response_model=DiaryResponse)
def get_today_diary(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """오늘 작성한 일기 조회"""
    return diary_service.get_today_diary(db, current_user_id)


@router.get("/date/{diary_date}", response_model=DiaryResponse)
def get_diary_by_date(
    diary_date: date,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """특정 날짜의 일기 조회"""
    return diary_service.get_diary_by_date(db, current_user_id, diary_date)
