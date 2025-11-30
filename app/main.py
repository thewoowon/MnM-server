from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan: Starting up...")
    # 데이터베이스 테이블 자동 생성
    from app.db.session import sync_engine
    from app.db.base import Base
    from app.models import User, Token, Movie, Diary, Ticket, UserTicket

    Base.metadata.create_all(bind=sync_engine)
    print("✅ Database tables created successfully!")

    yield
    print("Lifespan: Shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",  # React Native Metro bundler
        "http://localhost:3000",  # Web development
        "http://10.0.2.2:8081",  # Android emulator
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization", "RefreshToken"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


def start_uvicorn():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


def main():
    start_uvicorn()


if __name__ == "__main__":
    main()
