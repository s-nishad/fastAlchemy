from fastapi import FastAPI
from api import user, auth

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to fastAlchemy API"}


app.include_router(user.router)
app.include_router(auth.router)
