from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.movie import MovieResponse


class TicketBase(BaseModel):
    purpose: str
    explanation: str
    comment: Optional[str] = None


class TicketCreate(BaseModel):
    """티켓 생성 요청"""
    movie_id: int
    purpose: str
    explanation: str
    comment: Optional[str] = None


class TicketResponse(TicketBase):
    """티켓 응답 (영화 정보 포함)"""
    id: int
    user_id: int
    movie_id: int
    movie: MovieResponse  # 영화 정보 포함
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
