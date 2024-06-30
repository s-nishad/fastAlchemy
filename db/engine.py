from sqlalchemy.ext.asyncio import create_async_engine
from core.config import BASE_DIR

DATABASE_URL = f'sqlite+aiosqlite:///{BASE_DIR}/database.db'

engine = create_async_engine(DATABASE_URL, echo=True)
