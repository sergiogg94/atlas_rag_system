from app.core.logging import logger
from app.db.models import Collection
from app.db.repository import Repository
from app.services.chunking import TextChunker
from app.services.embeddings.factory import get_embedding_provider
from app.services.embeddings_service import EmbeddingsService
from app.services.llm.factory import get_llm_provider
from app.services.llm_service import LLMService


class RAGService:
    def __init__(self):
        self.llm_service = LLMService(provider=get_llm_provider())
        self.repo = Repository()

    def _get_embeddings_service(self, collection: Collection) -> EmbeddingsService:
        provider = get_embedding_provider(
            provider=collection.provider,
            model=collection.model,
            dimension=collection.dimension,
        )
        return EmbeddingsService(provider=provider)

    async def _get_collection_or_raise(self, collection_id: int) -> Collection:
        collection = await self.repo.get_collection(collection_id)

        if not collection:
            raise ValueError(f"Coolection with id={collection_id} not found.")
        return collection

    ###########################################################################
    # Collections managment
    ###########################################################################

    async def create_collection(
        self,
        name: str,
        provider: str,
        model: str,
        dimension: int,
        description: str | None = None,
    ):
        """Creates a new vector collection"""
        existing = await self.repo.get_collection_by_name(name)
        if existing:
            raise ValueError(f"A collection with the name '{name}' already exists.")

        return await self.repo.create_collection(
            name=name,
            provider=provider,
            model=model,
            dimension=dimension,
            description=description,
        )

    async def list_collections(self):
        return await self.repo.list_collections()

    async def delete_collection(self, collection_id: int) -> bool:
        return await self.repo.delete_collection(collection_id)

    ###########################################################################
    # Ingest
    ###########################################################################
    async def ingest(
        self,
        title: str,
        content: str,
        collection_id: int,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> tuple:
        """Ingest a document to the database"""
        logger.info("Ingest document process started")

        collection = await self._get_collection_or_raise(collection_id)
        embeddings_service = self._get_embeddings_service(collection)

        doc = await self.repo.create_document(title=title, collection_id=collection_id)

        chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = chunker.chunk_text(content)

        for chunk in chunks:
            embedding = await embeddings_service.encode(chunk)
            await self.repo.add_chunk(
                document_id=doc.id,
                content=chunk,
                embedding=embedding[0],
                dimension=collection.dimension,
            )

        logger.info("Document ingestion completed successfully.")
        return doc, len(chunks)

    ###########################################################################
    # Search and query
    ###########################################################################
    async def search(
        self, query: str, collection_id: int, top_k: int = 5, max_distance: float = 1.0
    ):
        """Search for relevant chunks on a given collection."""
        logger.info("Search process started")

        collection = await self._get_collection_or_raise(collection_id)
        embeddings_service = self._get_embeddings_service(collection)

        query_embedding = (await embeddings_service.encode(query))[0]

        logger.info("Query embedding generated successfully")
        return await self.repo.search(
            query_embedding=query_embedding,
            collection_id=collection_id,
            top_k=top_k,
            max_distance=max_distance,
        )

    async def query(
        self,
        question: str,
        collection_id: int,
        top_k: int = 5,
        max_distance: float = 1.0,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> str:
        logger.info("Query process started for question: %s...", question[:50])

        # Search for relevant chunks in the database
        search_results = await self.search(
            query=question,
            collection_id=collection_id,
            top_k=top_k,
            max_distance=max_distance,
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
        logger.info("Query process completed successfully")

        return {
            "answer": answer,
            "sources": search_results,
            "collection_id": collection_id,
        }

    def _build_context(self, search_results: list) -> str:
        """Build the context for the LLM based on the search results."""
        context_parts = []
        for i, chunk in enumerate(search_results, 1):
            # Formato simple
            context_parts.append(f"[{i}] {chunk.get('content')}")

        return "\n\n".join(context_parts)
