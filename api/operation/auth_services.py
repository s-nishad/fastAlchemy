from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from config import settings
from db.models.user import User
from schemas.auth_schema import (
    UserRegistrationRequest,
    UserLoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    PasswordChangeRequest,
    UserUpdateRequest,
)

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    # ----------------- Registration -----------------
    async def register_user(self, user_data: UserRegistrationRequest):
        if self.db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user = User(
            email=user_data.email,
            password=self.get_password_hash(user_data.password),
            name=user_data.name,
            phone=user_data.phone,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return {"message": "User registered successfully"}

    # ----------------- Login -----------------
    async def login_user(self, user_data: UserLoginRequest):
        user = self.db.query(User).filter(User.email == user_data.email).first()
        if not user or not self.verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        access_token = self.create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    # ----------------- Forgot Password -----------------
    async def initiate_password_reset(self, email: str):
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        reset_token = self.create_access_token(
            data={"sub": user.email, "type": "reset"}, expires_delta=timedelta(hours=1)
        )

        # TODO: Send reset_token via email
        return {"message": "Password reset instructions sent to email"}

    # ----------------- Reset Password -----------------
    async def reset_password(self, reset_data: ResetPasswordRequest):
        try:
            payload = jwt.decode(reset_data.token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if not email or payload.get("type") != "reset":
                raise HTTPException(status_code=400, detail="Invalid token")
        except JWTError:
            raise HTTPException(status_code=400, detail="Invalid token")

        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.hashed_password = self.get_password_hash(reset_data.new_password)
        self.db.commit()

        return {"message": "Password reset successful"}

    # ----------------- Change Password -----------------
    async def change_password(self, user_id: int, password_data: PasswordChangeRequest):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not self.verify_password(password_data.old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Current password is incorrect")

        user.hashed_password = self.get_password_hash(password_data.new_password)
        self.db.commit()

        return {"message": "Password changed successfully"}

    # ----------------- Update User -----------------
    async def update_user(self, user_id: int, update_data: UserUpdateRequest):
        user = self.db.query(User).filter(User.id == user_id).first()

        if update_data.email:
            existing_user = self.db.query(User).filter(User.email == update_data.email).first()
            if existing_user and existing_user.id != user_id:
                raise HTTPException(status_code=400, detail="Email already taken")
            user.email = update_data.email

        if update_data.name:
            user.name = update_data.name

        if update_data.phone:
            user.phone = update_data.phone

        self.db.commit()
        self.db.refresh(user)

        return user
