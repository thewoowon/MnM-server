from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class DiaryBase(BaseModel):
    content: str
    diary_date: Optional[date] = None


class DiaryCreate(DiaryBase):
    pass


class DiaryResponse(DiaryBase):
    id: int
    user_id: int
    diary_date: date
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
