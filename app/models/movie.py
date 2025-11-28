from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Movie(Base):
    __tablename__ = "movie"

    # 기본 필드
    name = Column(String, nullable=False)
    director = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
