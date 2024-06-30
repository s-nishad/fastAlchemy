import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


settings = Settings()
