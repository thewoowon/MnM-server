from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Ticket(Base):
    __tablename__ = "ticket"

    # 기본 필드
    purpose = Column(String, nullable=False)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # 관계 설정
    user_tickets = relationship("UserTicket", back_populates="ticket")
