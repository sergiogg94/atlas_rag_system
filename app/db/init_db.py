import asyncio

from sqlalchemy import text

from app.core.logging import logger
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

        # Create a general index for vectorial search
        logger.info("Creating vector index...")
        await conn.execute(
            text("""
            CREATE INDEX IF NOT EXISTS chunks_embedding_hnsw_idx
            ON chunks
            USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64)
        """)
        )
        logger.info("Index created successfuly")


if __name__ == "__main__":
    asyncio.run(init_db())
