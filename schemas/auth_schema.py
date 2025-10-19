from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegistrationRequest(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserBase(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    is_admin: Optional[bool] = False
    is_superuser: Optional[bool] = False

class UserInDBBase(UserBase):
    id: int

    class Config:
        from_attributes = True 

class UserResponse(UserInDBBase):
    pass

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None