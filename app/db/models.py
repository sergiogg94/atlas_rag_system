from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, ForeignKey, Index, Integer, Text
from sqlalchemy.orm import relationship

from app.db.engine import Base


class Document(Base):
    """Represents a document in the database.

    Attributes:
        id (int): The primary key of the document.
        title (str): The title of the document.
        chunks (List[Chunk]): A list of associated chunks for the document.
    """

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)

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
    embedding = Column(Vector(384), nullable=False)

    document = relationship("Document", back_populates="chunks")

    # Create index for similarity search
    __table_args__ = (
        Index(
            "chunks_embedding_idx",
            "embedding",
            postgresql_using="ivfflat",
            postgresql_ops={"embedding": "vector_cosine_ops"},
            postgresql_with={"lists": 100},
        ),
    )
