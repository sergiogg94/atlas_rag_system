import asyncio

from sqlalchemy import text

from app.core.logging import logger
from app.db.engine import engine


async def ensure_vector_index(dimension: int) -> None:
    """Create (if missing) the HNSW index for a given embedding dimension.

    The index is partial: it only indexes chunks whose ``dimension`` matches,
    so collections with different embedding dimensions can coexist in the same
    table. The expression index casts the column to a fixed dimension, which is
    required by pgvector for HNSW (weakly-typed ``vector`` columns cannot be
    indexed directly).
    """
    if dimension <= 0:
        raise ValueError(f"Dimension must be positive, got {dimension}")

    index_name = f"chunks_embedding_hnsw_{dimension}_idx"
    async with engine.begin() as conn:
        await conn.execute(
            text(
                f"""
                CREATE INDEX IF NOT EXISTS {index_name}
                ON chunks USING hnsw ((embedding::vector({dimension})) vector_cosine_ops)
                WITH (m = 16, ef_construction = 64)
                WHERE dimension = {dimension}
                """
            )
        )
        logger.info("Vector index ensured for dimension %d", dimension)


if __name__ == "__main__":
    import sys

    asyncio.run(ensure_vector_index(int(sys.argv[1])))
