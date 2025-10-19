from fastapi import FastAPI
from api import user

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to fastAlchemy API"}


app.include_router(user.router)
