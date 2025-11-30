from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.movie import Movie
from app.models.user import User
from typing import List
import random


def calculate_keyword_score(movie_keywords: List[str], user_keywords: List[str]) -> float:
    """
    영화 키워드와 사용자 키워드 간의 가중치 점수 계산
    매칭되는 키워드 개수를 점수로 반환
    """
    if not movie_keywords or not user_keywords:
        return 0.0

    # 대소문자 무시하고 매칭
    movie_keywords_lower = [k.lower() for k in movie_keywords]
    user_keywords_lower = [k.lower() for k in user_keywords]

    # 매칭되는 키워드 개수
    match_count = sum(1 for uk in user_keywords_lower if uk in movie_keywords_lower)

    return float(match_count)


def get_recommended_movies(
    db: Session,
    keywords: List[str],
    top_k: int = 5
) -> List[Movie]:
    """
    키워드 기반 영화 추천

    Args:
        db: Database session
        keywords: LLM이 추출한 키워드 리스트
        top_k: 반환할 영화 개수

    Returns:
        추천 영화 리스트
    """
    # 모든 영화 가져오기
    all_movies = db.query(Movie).all()

    if not all_movies:
        raise HTTPException(status_code=404, detail="No movies available")

    # 각 영화에 대해 점수 계산
    movie_scores = []
    for movie in all_movies:
        score = calculate_keyword_score(movie.keywords or [], keywords)
        movie_scores.append((movie, score))

    # 점수가 0보다 큰 영화만 필터링
    scored_movies = [(m, s) for m, s in movie_scores if s > 0]

    # 점수가 있는 영화가 없으면 랜덤 추천
    if not scored_movies:
        random_movies = random.sample(all_movies, min(top_k, len(all_movies)))
        return random_movies

    # 점수로 정렬 (내림차순)
    scored_movies.sort(key=lambda x: x[1], reverse=True)

    # 최고 점수 찾기
    max_score = scored_movies[0][1]

    # 최고 점수를 가진 영화들만 필터링
    top_scored_movies = [m for m, s in scored_movies if s == max_score]

    # 최고 점수 영화 중에서 랜덤으로 top_k개 선택
    k = min(top_k, len(top_scored_movies))
    recommended = random.sample(top_scored_movies, k)

    return recommended


def create_movie(db: Session, movie_data) -> Movie:
    """영화 생성"""
    new_movie = Movie(
        name=movie_data.name,
        director=movie_data.director,
        summary=movie_data.summary,
        cast=movie_data.cast,
        keywords=movie_data.keywords
    )

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return new_movie


def get_all_movies(db: Session, skip: int = 0, limit: int = 100) -> List[Movie]:
    """모든 영화 조회"""
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies


def get_movie_by_id(db: Session, movie_id: int) -> Movie:
    """ID로 영화 조회"""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
