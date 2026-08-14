from sqlalchemy import select

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

    ###########################################################################
    # Documents
    ###########################################################################

    async def create_document(self, title: str, collecctiion_id: int) -> Document:
        """Create a new document record in a collecon."""
        async with SessionLocal() as session:
            document = Document(title=title, collecctiion_id=collecctiion_id)
            session.add(document)
            await session.commit()
            await session.refresh(document)
            logger.info(
                "Document created: '%s' in collection %s", title, collecctiion_id
            )
            return document

    async def list_documents(self, collection_id: int) -> list[Document]:
        """List all documents in a collection."""
        async with SessionLocal() as session:
            result = await session.execute(
                select(Document)
                .where(Document.collection_id == collection_id)
                .order_by(Document.id.desc())
            )
            return list(result.scalars().all())

    ###########################################################################
    # Chunks
    ###########################################################################

    async def add_chunk(self, document_id: int, content: str, embedding: list[float]):
        """Add a new chunk associated with a document."""
        async with SessionLocal() as session:
            chunk = Chunk(document_id=document_id, content=content, embedding=embedding)
            session.add(chunk)
            await session.commit()

    async def search(
        self,
        query_embedding: list[float],
        collection_id: int,
        top_k: int = 5,
        max_distance: float = 1.0,
    ) -> list[str]:
        """Search stored chunks by cosine similarity against the query embedding
        inside a given collection.
        """
        async with SessionLocal() as session:
            # Add distance column
            distance_col = Chunk.embedding.cosine_distance(query_embedding).label(
                "distance"
            )

            logger.info("Executing search")
            result = await session.execute(
                select(Chunk, Document.title, distance_col)
                .join(Document, Chunk.document_id == Document.id)
                .where(Document.collection_id == collection_id)
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
