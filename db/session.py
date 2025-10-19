from typing import Generator
from sqlalchemy.orm import sessionmaker, Session
from db.engine import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> None:
    try:
        engine.connect()
        print("Database connected successfully!")
    except Exception as e:
        print(f"Error connecting to the database: {e}")


check_db_connection()
