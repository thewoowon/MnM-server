from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Ticket(Base):
    __tablename__ = "ticket"

    # 외래 키
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movie.id"), nullable=False)

    # 기본 필드
    purpose = Column(String, nullable=False)  # 영화를 보려는 목적
    explanation = Column(Text, nullable=False)  # LLM이 생성한 따뜻한 설명
    comment = Column(String, nullable=True)  # 사용자 코멘트 (선택)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # 관계 설정
    user = relationship("User", back_populates="tickets")
    movie = relationship("Movie", back_populates="tickets")
