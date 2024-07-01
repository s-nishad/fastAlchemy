from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from core.security import SECRET_KEY, verify_password, ALGORITHM
from db.models import User
from db.session import get_db
from schemas.auth import Login, Token, ChangePassword, ResetPassword, TokenData
from api.operation.auth import authenticate_user, get_user_by_username, get_user_by_email, create_access_token_for_user, \
    change_user_password

router = APIRouter(
    prefix="/auth", tags=["auth"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/login", response_model=Token)
async def login_for_access_token(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = await create_access_token_for_user(user)
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail={"error": str(e)})


# @router.get("/current-user", response_model=User)
# async def get_current_user(current_user: User = Depends(get_current_user)):
#     return current_user


@router.post("/change-password", response_model=Any)
async def change_password(
        change_password_data: ChangePassword,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if not verify_password(change_password_data.old_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect",
        )
    await change_user_password(db, current_user, change_password_data.new_password)
    return {"msg": "Password changed successfully"}
#
#
# @router.post("/reset-password", response_model=Any)
# async def reset_password(
#         db: AsyncSession = Depends(get_db),
#         reset_password_data: ResetPassword
# ):
#     user = await get_user_by_email(db, reset_password_data.email)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User with this email does not exist",
#         )
#     await change_user_password(db, user, reset_password_data.new_password)
#     return {"msg": "Password reset successfully"}
