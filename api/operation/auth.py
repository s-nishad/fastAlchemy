from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from db.models import User
from core.security import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas.auth import TokenData
from db.session import get_db


async def authenticate_user(db: AsyncSession, username: str, password: str):
    try:
        result = await db.execute(select(User).filter(User.username == username))
        user = result.scalars().first()
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user
    except Exception as e:
        raise HTTPException(401, detail={"error": str(e)})


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def create_access_token_for_user(user: User):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )


async def change_user_password(db: AsyncSession, user: User, new_password: str):
    user.password = get_password_hash(new_password)
    await db.commit()
    await db.refresh(user)
    return user
