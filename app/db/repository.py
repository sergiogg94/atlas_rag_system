from sqlalchemy import select
from app.db.engine import SessionLocal
from app.db.models import Document, Chunk
import numpy as np


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
            document = Document(title=title)
            session.add(document)
            await session.commit()
            await session.refresh(document)
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

    async def search(self, query_embedding: list[float], top_k: int = 5) -> list[str]:
        """Search stored chunks by cosine similarity against the query embedding.

        Args:
            query_embedding (list[float]): The embedding vector for the query.
            top_k (int, optional): The number of top matching chunks to return. Defaults to 5.

        Returns:
            list[str]: A list of chunk contents ranked by similarity to the query.
        """
        async with SessionLocal() as session:
            result = await session.execute(select(Chunk))
            chunks = result.scalars().all()

            # Simple cosine similarity search (for demonstration purposes)
            def sim_cos(a, b):
                a = np.array(a)
                b = np.array(b)
                return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

            scored_chunks = [
                (chunk, sim_cos(query_embedding, chunk.embedding)) for chunk in chunks
            ]
            scored_chunks.sort(key=lambda x: x[1], reverse=True)

            return [c.content for c, _ in scored_chunks[:top_k]]
