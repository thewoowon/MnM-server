from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.models.movie import Movie
from app.schemas.ticket import TicketCreate
from typing import List


def create_ticket(db: Session, user_id: int, ticket_data: TicketCreate) -> Ticket:
    """
    티켓 생성

    Args:
        db: DB 세션
        user_id: 티켓을 생성하는 사용자 ID
        ticket_data: 티켓 생성 데이터 (movie_id, purpose, explanation, comment)

    Returns:
        생성된 Ticket 객체
    """
    # 영화 존재 확인
    movie = db.query(Movie).filter(Movie.id == ticket_data.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # 티켓 생성
    new_ticket = Ticket(
        user_id=user_id,
        movie_id=ticket_data.movie_id,
        purpose=ticket_data.purpose,
        explanation=ticket_data.explanation,
        comment=ticket_data.comment
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


def get_user_tickets(db: Session, user_id: int) -> List[Ticket]:
    """
    사용자의 모든 티켓 조회 (최신순)

    Args:
        db: DB 세션
        user_id: 사용자 ID

    Returns:
        티켓 리스트
    """
    tickets = db.query(Ticket)\
        .filter(Ticket.user_id == user_id)\
        .order_by(Ticket.created_at.desc())\
        .all()

    return tickets


def get_ticket_by_id(db: Session, user_id: int, ticket_id: int) -> Ticket:
    """
    특정 티켓 조회 (본인 티켓만)

    Args:
        db: DB 세션
        user_id: 사용자 ID
        ticket_id: 티켓 ID

    Returns:
        Ticket 객체
    """
    ticket = db.query(Ticket)\
        .filter(Ticket.id == ticket_id, Ticket.user_id == user_id)\
        .first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


def delete_ticket(db: Session, user_id: int, ticket_id: int) -> None:
    """
    티켓 삭제 (본인 티켓만)

    Args:
        db: DB 세션
        user_id: 사용자 ID
        ticket_id: 티켓 ID
    """
    ticket = db.query(Ticket)\
        .filter(Ticket.id == ticket_id, Ticket.user_id == user_id)\
        .first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(ticket)
    db.commit()
