from typing import Optional

from app.core.config import settings
from app.core.logging import logger
from app.services.chunking import TextChunker
from app.services.embeddings.voyage_provider import VoyageProvider
from app.services.embeddings_service import EmbeddingsService
from app.services.llm.factory import get_llm_provider
from app.services.llm_service import LLMService


def _build_embedding_provider():
    return VoyageProvider(
        api_key=settings.voyage_api_key,
        model=settings.voyage_model,
        dimension=settings.voyage_embedding_dimension,
    )


class RAGService:

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        self.chunker = TextChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        self.embeddings_service = EmbeddingsService(
            provider=_build_embedding_provider()
        )
        self.llm_service = LLMService(provider=get_llm_provider())

    async def ingest(
        self,
        title: str,
        content: str,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
    ) -> tuple:
        """Ingest a document to the database

        Args:
            title (str): Title of the document.
            content (str): Content of the document.
            chunk_size (Optional[int]): Override chunk size for this ingest.
            chunk_overlap (Optional[int]): Override chunk overlap for this ingest.
        """
        logger.info("Ingest document process started")
        from app.db.repository import Repository

        repo = Repository()

        doc = await repo.create_document(title=title)

        if chunk_size is not None or chunk_overlap is not None:
            chunker = TextChunker(
                chunk_size=(
                    chunk_size if chunk_size is not None else self.chunker.chunk_size
                ),
                chunk_overlap=(
                    chunk_overlap
                    if chunk_overlap is not None
                    else self.chunker.chunk_overlap
                ),
            )
        else:
            chunker = self.chunker

        chunks = chunker.chunk_text(content)
        for chunk in chunks:
            embedding = await self.embeddings_service.encode(chunk)
            await repo.add_chunk(
                document_id=doc.id, content=chunk, embedding=embedding[0]
            )
        logger.info("Document ingestion completed successfully.")

        return doc, len(chunks)

    async def search(
        self, query: str, top_k: int = 5, probes: int = 10, max_distance: float = 1.0
    ):
        logger.info("Search process started")
        from app.db.repository import Repository

        repo = Repository()

        query_embedding = (await self.embeddings_service.encode(query))[0]
        logger.info("Query embedding generated successfully")
        results = await repo.search(
            query_embedding=query_embedding,
            top_k=top_k,
            probes=probes,
            max_distance=max_distance,
        )
        return results

    def _build_context(self, search_results: list) -> str:
        """Build the context for the LLM based on the search results."""
        context_parts = []
        for i, chunk in enumerate(search_results, 1):
            # Formato simple
            context_parts.append(f"[{i}] {chunk.get('content')}")

        return "\n\n".join(context_parts)

    async def query(
        self,
        question: str,
        top_k: int = 5,
        max_distance: float = 1.0,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> str:
        logger.info(f"Query process started for question: {question[:50]}...")

        # Search for relevant chunks in the database
        search_results = await self.search(
            query=question, top_k=top_k, max_distance=max_distance
        )

        # Build context for the LLM based on the search results
        context = self._build_context(search_results)

        # Generate an answer using the LLM based on the question and the context
        answer = await self.llm_service.get_answer(
            query=question,
            context=context,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        sources = [
            {
                "chunk_id": result["chunk_id"],
                "document_id": result["document_id"],
                "document_title": result["document_title"],
                "distance": result["distance"],
                "content": result["content"],
            }
            for result in search_results
        ]
        logger.info(f"Query process completed successfully")

        return {
            "answer": answer,
            "sources": sources,
        }
