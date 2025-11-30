from fastapi import APIRouter
from app.api.v1.endpoints import user, auth, movie, diary, ticket

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(movie.router, prefix="/movies", tags=["movies"])
api_router.include_router(diary.router, prefix="/diaries", tags=["diaries"])
api_router.include_router(ticket.router, prefix="/tickets", tags=["tickets"])
