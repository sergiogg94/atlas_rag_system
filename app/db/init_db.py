import asyncio
from sqlalchemy import text
from app.db.models import Document, Chunk
from app.db.engine import engine, Base
from app.core.logging import logger


async def init_db():
    """Initialize the database.

    This function creates the pgvector extension and all tables defined in the SQLAlchemy models.
    """
    async with engine.begin() as conn:
        logger.info("Creating pgvector extension...")
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        logger.info("pgvector extension created successfully.")

        logger.info("Creating database tables...")
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully.")


if __name__ == "__main__":
    asyncio.run(init_db())
