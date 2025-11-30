from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TicketBase(BaseModel):
    purpose: str
    comment: Optional[str] = None


class TicketCreate(TicketBase):
    pass


class TicketResponse(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserTicketResponse(BaseModel):
    """유저가 가진 티켓 정보"""
    ticket: TicketResponse
    created_at: datetime

    class Config:
        from_attributes = True
