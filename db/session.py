from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from db.engine import engine

# Create a new async session
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def check_db_connection() -> None:
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("Database connected successfully!")
    except Exception as e:
        print(f"Error connecting to the database: {e}")


# Ensure the database connection on startup
import asyncio

if __name__ == "__main__":
    try:
        asyncio.run(check_db_connection())
    except RuntimeError as e:
        if str(e).startswith("asyncio.run() cannot be called from a running event loop"):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(check_db_connection())
        else:
            raise
