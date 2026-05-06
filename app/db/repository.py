from sqlalchemy import select, text
from app.db.engine import SessionLocal
from app.db.models import Document, Chunk
import numpy as np
from app.core.logging import logger


class Repository:
    """Repository class for managing database interactions."""

    async def create_document(self, title: str) -> Document:
        """Create a new document record in the database.

        Args:
            title (str): The title of the document to create.

        Returns:
            Document: The created Document instance.
        """
        async with SessionLocal() as session:
            logger.info(f"Creating document with title: {title}")
            document = Document(title=title)
            session.add(document)
            await session.commit()
            await session.refresh(document)
            logger.info(f"Document created with ID: {document.id}")
            return document

    async def add_chunk(self, document_id: int, content: str, embedding: list[float]):
        """Add a new chunk associated with a document.

        Args:
            document_id (int): The ID of the parent document.
            content (str): The text content of the chunk.
            embedding (list[float]): The vector embedding for the chunk.
        """
        async with SessionLocal() as session:
            chunk = Chunk(document_id=document_id, content=content, embedding=embedding)
            session.add(chunk)
            await session.commit()

    async def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        probes: int = 10,
        max_distance: float = 1.0,
    ) -> list[str]:
        """Search stored chunks by cosine similarity against the query embedding.

        Args:
            query_embedding (list[float]): The embedding vector for the query.
            top_k (int, optional): The number of top matching chunks to return. Defaults to 5.
            probes (int, optional): The number of probes to use for the search. Defaults to 10.
            max_distance (float, optional): The maximum cosine distance for a chunk to be considered a match. Defaults to 0.5.

        Returns:
            list[str]: A list of chunk contents ranked by similarity to the query.
        """
        async with SessionLocal() as session:
            # Configure the number of probes for the search
            await session.execute(text(f"SET ivfflat.probes = {probes}"))

            # Add distance column
            distance_col = Chunk.embedding.cosine_distance(query_embedding).label(
                "distance"
            )

            logger.info("Executing search")
            result = await session.execute(
                select(Chunk, distance_col)
                .where(distance_col <= max_distance)
                .order_by(distance_col)
                .limit(top_k)
            )

            return [
                {
                    "document_id": chunk.document_id,
                    "chunk_id": chunk.id,
                    "content": chunk.content,
                    "distance": float(distance),
                }
                for chunk, distance in result.all()
            ]
