from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.models.user_ticket import UserTicket
from app.models.user import User
from app.schemas.ticket import TicketCreate
from typing import List


def create_ticket(db: Session, ticket_data: TicketCreate) -> Ticket:
    """티켓 생성"""
    new_ticket = Ticket(
        purpose=ticket_data.purpose,
        comment=ticket_data.comment
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


def assign_ticket_to_user(db: Session, user_id: int, ticket_id: int) -> UserTicket:
    """유저에게 티켓 할당"""
    # 유저 존재 확인
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 티켓 존재 확인
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # 이미 할당된 티켓인지 확인
    existing = db.query(UserTicket).filter(
        UserTicket.user_id == user_id,
        UserTicket.ticket_id == ticket_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Ticket already assigned to user"
        )

    # 티켓 할당
    user_ticket = UserTicket(
        user_id=user_id,
        ticket_id=ticket_id
    )

    db.add(user_ticket)
    db.commit()
    db.refresh(user_ticket)

    return user_ticket


def create_and_assign_ticket(
    db: Session,
    user_id: int,
    ticket_data: TicketCreate
) -> UserTicket:
    """티켓 생성 후 유저에게 바로 할당"""
    # 티켓 생성
    new_ticket = create_ticket(db, ticket_data)

    # 유저에게 할당
    user_ticket = assign_ticket_to_user(db, user_id, new_ticket.id)

    return user_ticket


def get_user_tickets(db: Session, user_id: int) -> List[UserTicket]:
    """유저가 가진 모든 티켓 조회"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_tickets = db.query(UserTicket)\
        .filter(UserTicket.user_id == user_id)\
        .order_by(UserTicket.created_at.desc())\
        .all()

    return user_tickets


def get_ticket_by_id(db: Session, ticket_id: int) -> Ticket:
    """ID로 티켓 조회"""
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket
