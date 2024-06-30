from fastapi import APIRouter

router = APIRouter(
    prefix="/auth", tags=["auth"]
)


@router.post("/login")
async def login(username: str, password: str):
    pass
