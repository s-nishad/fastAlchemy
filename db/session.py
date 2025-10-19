from contextlib import contextmanager
import typing
from sqlalchemy.orm import sessionmaker
from db.engine import engine
from sqlalchemy.orm import Session

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


@contextmanager
def get_db() -> typing.Generator[Session, None, None]:
    db = Session(autocommit=False, autoflush=False, bind=engine, future=True)
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
