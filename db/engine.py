from sqlalchemy import create_engine
from core.config import BASE_DIR

engine = create_engine(f'sqlite:///{BASE_DIR}/database.db')
