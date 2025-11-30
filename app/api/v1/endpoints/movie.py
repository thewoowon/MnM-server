from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.movie import (
    MovieCreate,
    MovieResponse,
    MovieRecommendationRequest,
    MovieRecommendationResponse
)
from app.services import movie_service
from app.services.llm_service import extract_keywords_from_diary

router = APIRouter()


@router.post("/recommend", response_model=MovieRecommendationResponse)
def recommend_movies(
    request: MovieRecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    일기 + purpose 기반 영화 추천

    OpenAI를 사용하여 일기에서 키워드를 추출한 후,
    키워드 매칭 점수를 기반으로 영화를 추천합니다.
    """
    # OpenAI로 키워드 추출
    keywords = extract_keywords_from_diary(
        request.diary_content,
        request.purpose
    )

    # 키워드 기반 영화 추천
    recommended_movies = movie_service.get_recommended_movies(
        db,
        keywords,
        request.top_k
    )

    return MovieRecommendationResponse(
        movies=recommended_movies,
        keywords=keywords
    )


@router.post("/recommend-by-keywords", response_model=List[MovieResponse])
def recommend_by_keywords(
    keywords: List[str],
    top_k: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    키워드 배열을 직접 받아서 영화 추천
    (프론트엔드에서 LLM 처리를 완료한 경우)
    """
    recommended_movies = movie_service.get_recommended_movies(
        db,
        keywords,
        top_k
    )
    return recommended_movies


@router.post("/", response_model=MovieResponse)
def create_movie(
    movie_data: MovieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """영화 생성 (관리자용)"""
    return movie_service.create_movie(db, movie_data)


@router.get("/", response_model=List[MovieResponse])
def get_all_movies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """모든 영화 조회"""
    return movie_service.get_all_movies(db, skip, limit)


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """영화 상세 조회"""
    return movie_service.get_movie_by_id(db, movie_id)
