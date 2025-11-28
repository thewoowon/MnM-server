from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.services.user_service import create_user
from app.core.security import decode_token
import requests
import jwt
from datetime import datetime, timedelta, timezone
from settings import (
    DEFAULT_PROFILE_PIC,
    GOOGLE_TOKEN_INFO_URL,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from app.models.user import User
from app.schemas.user import UserCreate
from app.models.token import Token
import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


def create_access_token(data: dict, expires_delta: timedelta):
    print("Creating access token with data:", data)
    to_encode = data.copy()
    print("Data to encode:", to_encode)
    expire = datetime.now(timezone.utc) + expires_delta
    print("Token expiration time:", expire)
    to_encode.update({"exp": expire})
    print("Final payload to encode:", to_encode)
    print("JWT Secret Key:", JWT_SECRET_KEY)
    print("JWT Algorithm:", JWT_ALGORITHM)
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    print("Encoded JWT:", encoded_jwt)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def google_auth(request: Request, db: Session):
    try:
        
        data = await request.json()
        print("Received Google auth data:", data)
        
        email = data.get("email")
        print("Extracted email from request data:", email)

        if not email:
            raise HTTPException(status_code=400, detail="Email is missing in token")

        # 사용자 조회 또는 생성
        user = db.query(User).filter(User.email == email).first()

        if not user:
            print("Creating new user for email:", email)
            # 새로운 사용자 생성
            user = create_user(
                db=db,
                user=UserCreate(
                    name=data.get("name", "Unknown"),
                    email=email,
                    profile_pic=data.get("photoUrl",DEFAULT_PROFILE_PIC),
                    provider="google",
                    provider_id=data.get("sub", ""),
                ),
            )
        print("User found/created:", user.email)

        # 토큰 생성
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        print("Generating tokens for user:", user.email)

        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires,
        )

        print("Access token generated for user:", user.email)
        refresh_token = create_refresh_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=refresh_token_expires,
        )

        print("Generated tokens for user:", user.email)
        print("Access Token:", access_token)
        print("Refresh Token:", refresh_token)

        # Refresh Token을 DB에 저장
        existing_token = db.query(Token).filter(Token.user_id == user.id).first()
        if existing_token:
            existing_token.refresh_token = refresh_token
            existing_token.is_active = True
        else:
            new_token = Token(
                user_id=user.id, refresh_token=refresh_token, is_active=True
            )
            db.add(new_token)
        db.commit()

        print("Saved refresh token to database for user:", user.email)

        # 사용자 데이터 및 토큰 반환
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "profile_pic": user.profile_pic,
            "provider": user.provider,
        }

        print("Returning user data and tokens")

        # RN 앱 형식에 맞게 헤더로 토큰 반환
        return JSONResponse(
            content={"user": user_data},
            status_code=200,
            headers={
                "Authorization": f"Bearer {access_token}",
                "RefreshToken": f"RefreshToken {refresh_token}",
            },
        )
    except Exception as e:
        print("Error:", e)
        print("Failed to verify token")
        raise HTTPException(status_code=400, detail="Invalid token")


async def refresh_token_func(request: Request, db: Session):
    try:
        # Request Body에서 refreshToken 추출
        data = await request.json()
        refresh_token = data.get("refreshToken")

        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is required",
            )

        # Refresh Token 디코딩 및 검증
        try:
            payload = jwt.decode(
                refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        user_id = payload.get("user_id")
        email = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        # DB에서 refresh_token 조회
        token_obj = (
            db.query(Token)
            .filter(Token.user_id == user_id, Token.refresh_token == refresh_token)
            .first()
        )

        if not token_obj:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        if not token_obj.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive refresh token",
            )

        # 새로운 Access Token & Refresh Token 발급
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        new_access_token = create_access_token(
            data={"sub": email, "user_id": user_id}, expires_delta=access_token_expires
        )
        new_refresh_token = create_refresh_token(
            data={"sub": email, "user_id": user_id},
            expires_delta=refresh_token_expires,
        )

        # DB의 refresh_token 업데이트
        token_obj.refresh_token = new_refresh_token
        db.commit()

        # RN 앱 형식에 맞게 헤더로 반환
        return JSONResponse(
            content={"message": "Token refreshed successfully"},
            status_code=200,
            headers={
                "Authorization": f"Bearer {new_access_token}",
                "RefreshToken": f"RefreshToken {new_refresh_token}",
            },
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        print("Error:", e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
