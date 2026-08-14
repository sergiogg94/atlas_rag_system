import asyncio

from sqlalchemy import text

from app.core.logging import logger
from app.db import models  # noqa: F401  (registers tables on Base.metadata)
from app.db.engine import Base, engine


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
