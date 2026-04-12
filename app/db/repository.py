from sqlalchemy import select
from app.db.engine import SessionLocal
from app.db.models import Document, Chunk
import numpy as np


class Repository:
    async def create_document(self, title: str):
        async with SessionLocal() as session:
            document = Document(title=title)
            session.add(document)
            await session.commit()
            await session.refresh(document)
            return document

    async def add_chunk(self, document_id: int, content: str, embedding: list[float]):
        async with SessionLocal() as session:
            chunk = Chunk(document_id=document_id, content=content, embedding=embedding)
            session.add(chunk)
            await session.commit()

    async def search(self, query_embedding: list[float], top_k: int = 5):
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
