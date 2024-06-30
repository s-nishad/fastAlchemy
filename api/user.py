from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from schemas.user import User, UserCreate, UserUpdate
from db.session import get_db
from api.operation.user import get_user_by_email, create_user as create_user_operation, get_user, get_users, \
    update_user as update_user_operation, delete_user as delete_user_operation

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_user_operation(db=db, user=user)


@router.get("/{user_guid}", response_model=User)
async def get_user_by_guid(user_guid: str, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user_guid=user_guid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/", response_model=List[User])
async def get_all_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    users = await get_users(db, skip=skip, limit=limit)
    return users


@router.put("/{user_guid}", response_model=User)
async def update_user(user_guid: str, user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user_guid=user_guid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await update_user_operation(db=db, db_user=db_user, user_update=user_update)


@router.delete("/{user_guid}", response_model=User)
async def delete_user(user_guid: str, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db, user_guid=user_guid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await delete_user_operation(db=db, user_guid=user_guid)
