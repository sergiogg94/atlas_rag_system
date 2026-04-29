import random
from app.core.logging import logger
from app.services.chunking import TextChunker
from app.services.embeddings import EmbeddingsService


class RAGService:

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        min_chunk_size: int = 100,
    ):
        self.chunker = TextChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            min_chunk_size=min_chunk_size,
        )
        self.embeddings_service = EmbeddingsService()

    async def query(self, question: str):
        return "Not implemented"

    async def ingest(self, title: str, content: str) -> tuple:
        """Ingest a document to the database

        Args:
            title (str): Title of the document.
            content (str): Content of the document.
        """
        logger.info("Ingest document process started")
        from app.db.repository import Repository

        repo = Repository()

        doc = await repo.create_document(title=title)

        chunks = self.chunker.chunk_by_characters(content)
        for chunk in chunks:
            embedding = await self.embeddings_service.encode(chunk)
            await repo.add_chunk(
                document_id=doc.id, content=chunk, embedding=embedding[0]
            )
        logger.info("Document ingestion completed successfully.")

        return doc, len(chunks)

    async def search(
        self, query: str, top_k: int = 5, probes: int = 10, max_distance: float = 0.5
    ):
        logger.info("Search process started")
        from app.db.repository import Repository

        repo = Repository()

        query_embedding = await self.embeddings_service.encode(query)
        results = await repo.search(
            query_embedding=query_embedding,
            top_k=top_k,
            probes=probes,
            max_distance=max_distance,
        )
        return results
