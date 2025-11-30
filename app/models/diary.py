from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Diary(Base):
    __tablename__ = "diary"

    # 외래 키
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    # 기본 필드
    content = Column(String, nullable=False)  # 일기 내용
    purpose = Column(String, nullable=False)  # 목적
    mood = Column(String, nullable=True)
    diary_date = Column(Date, nullable=False, default=func.current_date())  # 일기 작성 날짜

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # 관계 설정
    user = relationship("User", back_populates="diaries")
