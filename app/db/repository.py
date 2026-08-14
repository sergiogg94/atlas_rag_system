from sqlalchemy import select, text

from app.core.logging import logger
from app.db.engine import SessionLocal
from app.db.models import Chunk, Collection, Document


class Repository:
    """Repository class for managing database interactions."""

    ###########################################################################
    # Collections
    ###########################################################################

    async def create_collection(
        self,
        name: str,
        provider: str,
        model: str,
        dimension: int,
        description: str | None = None,
    ):
        """Creates a new vector collection."""
        async with SessionLocal() as session:
            collection = Collection(
                name=name,
                provider=provider,
                model=model,
                dimension=dimension,
                description=description,
            )
            session.add(collection)
            await session.commit()
            await session.refresh(collection)
            logger.info("Collection created: '%s' (id=%s)", name, collection.id)

            return collection

    async def get_collection(self, collection_id: int) -> Collection | None:
        """Get collection by ID."""
        async with SessionLocal() as session:
            result = await session.execute(
                select(Collection).where(Collection.id == collection_id)
            )
            return result.scalar_one_or_none()

    async def get_collection_by_name(self, name: str) -> Collection | None:
        """Get collection by name."""
        async with SessionLocal() as session:
            result = await session.execute(
                select(Collection).where(Collection.name == name)
            )
            return result.scalar_one_or_none()

    async def list_collections(self) -> list[Collection]:
        """List all collections"""
        async with SessionLocal() as session:
            result = await session.execute(
                select(Collection).order_by(Collection.created_at.desc())
            )
            return list(result.scalars().all())

    async def delete_collection(self, collection_id: int) -> bool:
        """Deletes a collection and all its documents/chunks (cascade)."""
        async with SessionLocal() as session:
            result = await session.execute(
                select(Collection).where(Collection.id == collection_id)
            )
            collection = result.scalar_one_or_none()
            if not collection:
                return False
            await session.delete(collection)
            await session.commit()
            logger.info("Collection deleted: id=%s", collection_id)
            return True

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
            probes = max(1, int(probes))
            await session.execute(text(f"SET LOCAL ivfflat.probes = {probes}"))

            # Add distance column
            distance_col = Chunk.embedding.cosine_distance(query_embedding).label(
                "distance"
            )

            logger.info("Executing search")
            result = await session.execute(
                select(Chunk, Document.title, distance_col)
                .join(Document, Chunk.document_id == Document.id)
                .where(distance_col <= max_distance)
                .order_by(distance_col)
                .limit(top_k)
            )

            return [
                {
                    "document_id": chunk.document_id,
                    "document_title": title,
                    "chunk_id": chunk.id,
                    "content": chunk.content,
                    "distance": float(distance),
                }
                for chunk, title, distance in result.all()
            ]
