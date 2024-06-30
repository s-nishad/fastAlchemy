from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: str
    email: EmailStr
    is_admin: Optional[bool] = False
    is_superuser: Optional[bool] = False


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: int
    guid: str

    class Config:
        orm_mode: True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    password: str
