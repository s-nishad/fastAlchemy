from fastapi import APIRouter

router = APIRouter(
    prefix="/user", tags=["user"]
)


@router.get('/all')
async def get_users():
    return {'message': 'Hello World'}


@router.get('/api/user')
async def get_all_users():
    return {'message': 'Hello World'}
