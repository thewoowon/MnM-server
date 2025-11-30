from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class UserTicket(Base):
    __tablename__ = "user_ticket"

    # 외래 키
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    ticket_id = Column(Integer, ForeignKey("ticket.id"), nullable=False)

    # 타임스탬프
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # 관계 설정
    user = relationship("User", back_populates="user_tickets")
    ticket = relationship("Ticket", back_populates="user_tickets")
