from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class MovieBase(BaseModel):
    name: str
    director: str
    summary: str
    cast: Optional[str] = None
    keywords: Optional[List[str]] = []
    url: Optional[str] = None


class MovieCreate(MovieBase):
    pass


class MovieResponse(MovieBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MovieRecommendationRequest(BaseModel):
    """영화 추천 요청"""
    diary_content: str
    purpose: str
    top_k: Optional[int] = 5  # 추천할 영화 개수


class MovieRecommendationResponse(BaseModel):
    """영화 추천 응답"""
    movies: List[MovieResponse]
    keywords: List[str]  # LLM이 추출한 키워드들
    explanation: str  # 키워드 선택 이유에 대한 따뜻한 설명
