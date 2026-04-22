import random
from app.core.logging import logger
from app.services.chunking import TextChunker


class RAGService:

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        min_chunk_size: int = 100,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size

    # TODO: Implement this fake methods as a separate services
    def fake_embedding(self, text: str):
        # This is a placeholder for an actual embedding function
        return [random.random() for _ in range(768)]

    async def query(self, question: str):
        return "Not implemented"

    async def ingest(self, title: str, content: str) -> None:
        """Ingest a document to the database

        Args:
            title (str): Title of the document.
            content (str): Content of the document.
        """
        logger.info("Ingest document process started")
        from app.db.repository import Repository

        repo = Repository()

        doc = await repo.create_document(title=title)

        chunker = TextChunker(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            min_chunk_size=self.min_chunk_size,
        )
        chunks = chunker.chunk_by_characters(content)
        for chunk in chunks:
            embedding = self.fake_embedding(chunk)
            await repo.add_chunk(document_id=doc.id, content=chunk, embedding=embedding)
        logger.info("Document ingestion completed successfully.")

    async def search(self, query: str):
        logger.info("Search process started")
        from app.db.repository import Repository

        repo = Repository()

        query_embedding = self.fake_embedding(query)
        results = await repo.search(query_embedding=query_embedding, top_k=5)
        return results
