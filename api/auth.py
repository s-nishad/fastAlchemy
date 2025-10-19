from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from db.session import get_db
from db.models.user import User
from schemas.auth_schema import (
    UserRegistrationRequest,
    UserLoginRequest,
    UserResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    PasswordChangeRequest,
    UserUpdateRequest,
)
from api.operation.auth_services import AuthService
from config import settings
from jose import JWTError, jwt


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ----------------- JWT Dependency -----------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


# ----------------- Routes -----------------
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegistrationRequest, db: Session = Depends(get_db)):
    return await AuthService(db).register_user(user_data)


@router.post("/login")
async def login(user_data: UserLoginRequest, db: Session = Depends(get_db)):
    return await AuthService(db).login_user(user_data)


@router.post("/forgot-password")
async def forgot_password(email_data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    return await AuthService(db).initiate_password_reset(email_data.email)


@router.post("/reset-password")
async def reset_password(reset_data: ResetPasswordRequest, db: Session = Depends(get_db)):
    return await AuthService(db).reset_password(reset_data)


@router.post("/change-password")
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return await AuthService(db).change_password(current_user.id, password_data)


@router.patch("/update-profile")
async def update_profile(
    update_data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return await AuthService(db).update_user(current_user.id, update_data)


# ----------------- Current User -----------------
@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Returns the current logged-in user's details.
    """
    return current_user