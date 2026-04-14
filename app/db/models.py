from sqlalchemy import Column, Integer, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.engine import Base
from sqlalchemy.dialects.postgresql import ARRAY


class Document(Base):
    """Represents a document in the database.

    Attributes::
        id (int): The primary key of the document.
        title (str): The title of the document.
        chunks (List[Chunk]): A list of associated chunks for the document.
    """

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)

    chunks = relationship("Chunk", back_populates="document")


class Chunk(Base):
    """Represents a chunk of text associated with a document.

    Attributes::
        id (int): The primary key of the chunk.
        document_id (int): The foreign key referencing the associated document.
        content (str): The content of the chunk.
        embedding (List[float]): The embedding vector for the chunk.
    """

    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    content = Column(Text)
    embedding = Column(ARRAY(Float))

    document = relationship("Document", back_populates="chunks")
