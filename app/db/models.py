from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import relationship

from app.db.engine import Base


class Collection(Base):
    """Represents a collection of vectors with a specific provider and dimension.

    Each collection has its own embedding space: provider, model, and dimension
    are immutable after creation because all chunks must be comparable.
    """

    _tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    provider = Column(Text, nullable=False)  # "voyage" | "local"
    model = Column(Text, nullable=False)  # exac model name
    dimension = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    documents = relationship(
        "Document", back_populates="collection", cascade="all, delete-orphan"
    )


class Document(Base):
    """Represents a document in the database.

    Attributes:
        id (int): The primary key of the document.
        title (str): The title of the document.
        chunks (List[Chunk]): A list of associated chunks for the document.
    """

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    collection_id = Column(Integer, ForeignKey("collections.id"), nullable=False)
    title = Column(Text, nullable=False)

    collection = relationship("Collection", back_populates="documents")
    chunks = relationship(
        "Chunk", back_populates="document", cascade="all, delete-orphan"
    )


class Chunk(Base):
    """Represents a chunk of text associated with a document.

    Attributes:
        id (int): The primary key of the chunk.
        document_id (int): The foreign key referencing the associated document.
        content (str): The content of the chunk.
        embedding (Vector(384)): The embedding vector for the chunk.
    """

    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector, nullable=False)

    document = relationship("Document", back_populates="chunks")
