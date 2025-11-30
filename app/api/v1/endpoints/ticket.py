from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketResponse, UserTicketResponse
from app.services import ticket_service

router = APIRouter()


@router.post("/", response_model=TicketResponse)
def create_and_assign_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """티켓 생성 및 자동으로 현재 유저에게 할당"""
    user_ticket = ticket_service.create_and_assign_ticket(
        db,
        current_user.id,
        ticket_data
    )
    return user_ticket.ticket


@router.get("/my-tickets", response_model=List[UserTicketResponse])
def get_my_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """내가 가진 모든 티켓 조회"""
    user_tickets = ticket_service.get_user_tickets(db, current_user.id)

    # UserTicketResponse 형식으로 변환
    return [
        UserTicketResponse(
            ticket=ut.ticket,
            created_at=ut.created_at
        )
        for ut in user_tickets
    ]


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """티켓 상세 조회"""
    return ticket_service.get_ticket_by_id(db, ticket_id)
