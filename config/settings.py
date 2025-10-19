import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


# Auth Data 
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "deepseek/deepseek-chat-v3-0324:free")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
USE_TEMPERATURE = os.getenv("USE_TEMPERATURE", "TRUE").upper() == "TRUE"
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))

DATABASE_URL = "sqlite+aiosqlite:///./contextiq.db"


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
JWT_ALGORITHM = "HS256"
JWT_EXP_MINUTES = 60

UPLOAD_DIR = os.path.join(ROOT_DIR, "storage", "uploads")
FAISS_DIR = os.path.join(ROOT_DIR, "storage", "faiss")
CHUNK_SIZE = 500