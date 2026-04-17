import asyncio
from app.db.models import Document, Chunk
from app.db.engine import engine, Base


async def init_db():
    """Initialize the database.

    This function creates all tables defined in the SQLAlchemy models.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
