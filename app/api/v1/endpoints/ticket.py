from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.core.security import get_current_user
from app.schemas.ticket import TicketCreate, TicketResponse
from app.services import ticket_service

router = APIRouter()


@router.post("/", response_model=TicketResponse)
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """
    티켓 생성 (영화 추천 저장)

    영화 추천을 받은 후, 마음에 드는 영화를 티켓으로 저장합니다.
    """
    return ticket_service.create_ticket(db, current_user_id, ticket_data)


@router.get("/", response_model=List[TicketResponse])
def get_my_tickets(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """
    내 티켓 목록 조회 (최신순)

    내가 저장한 모든 티켓을 조회합니다.
    """
    return ticket_service.get_user_tickets(db, current_user_id)


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """
    티켓 상세 조회 (본인 티켓만)
    """
    return ticket_service.get_ticket_by_id(db, current_user_id, ticket_id)


@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    """
    티켓 삭제 (본인 티켓만)
    """
    ticket_service.delete_ticket(db, current_user_id, ticket_id)
    return {"message": "Ticket deleted successfully"}
