from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import User
from schemas.user import UserCreate, UserUpdate
from core.security import get_password_hash


async def get_user(db: AsyncSession, user_guid: str):
    result = await db.execute(select(User).filter(User.guid == user_guid))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),  # You should hash the password before storing it
        is_admin=user.is_admin,
        is_superuser=user.is_superuser,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, db_user: User, user_update: UserUpdate):
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_guid: str):
    result = await db.execute(select(User).filter(User.guid == user_guid))
    db_user = result.scalars().first()
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user
