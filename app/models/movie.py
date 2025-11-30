from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Movie(Base):
    __tablename__ = "movie"

    # 영화명
    name = Column(String, nullable=False)
    # 감독명
    director = Column(String, nullable=False)
    # 줄거리
    summary = Column(String, nullable=False)
    # 출연진
    cast = Column(String, nullable=True)

    # 키워드 (JSON 배열로 저장)
    keywords = Column(JSON, nullable=True, default=[])

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
