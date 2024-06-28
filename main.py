from fastapi import FastAPI
from api.user import router as user_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to fastAlchemy API"}


app.include_router(user_router)
