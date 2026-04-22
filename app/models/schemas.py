from pydantic import BaseModel, Field
from typing import Optional


class QueryRequest(BaseModel):
    """Request model for a question to query the RAG service.

    Attributes:
        question (str): The user's question to process.
    """

    question: str = Field(
        ...,
        description="User question to be processed",
        example="What is the capital of France?",
        min_length=1,
        max_length=500,
    )


class QueryResponse(BaseModel):
    """Response model returned by the RAG service.

    Attributes:
        response (str): The generated answer text.
        sources (list[str]): A list of sources used to generate the answer.
    """

    response: str = Field(
        ...,
        description="Answer generated",
        example="The capital of France is Paris.",
    )
    sources: list[str] = Field(
        [],
        description="List of sources used to generate the answer",
    )


class IngestRequest(BaseModel):
    """Request model for ingesting a new document into the RAG system.

    Attributes:
        title (str): The title of the document to be ingested.
        content (str): The content of the document to be ingested.
        chunk_size (int): The size of text chunks for processing. Defaults to 500.
        chunk_overlap (int): The overlap between chunks. Defaults to 50.
        min_chunk_size (int): The minimum size for a chunk. Defaults to 100.
    """

    title: str = Field(
        ...,
        description="Title of the document to be ingested",
        example="Geography for dummies",
        min_length=1,
        max_length=200,
    )
    content: str = Field(
        ...,
        description="Content of the document to be ingested",
        example="France is a country in Europe. The capital of France is Paris.",
        min_length=1,
    )
    chunk_size: int = Field(
        500,
        description="Size of text chunks for processing",
        ge=1,
    )
    chunk_overlap: int = Field(
        50,
        description="Overlap between chunks",
        ge=0,
    )
    min_chunk_size: int = Field(
        100,
        description="Minimum size for a chunk",
        ge=1,
    )


class SearchRequest(BaseModel):
    """Request model for searching documents in the RAG system.

    Attributes:
        query (str): The search query to find relevant documents.
    """

    query: str = Field(
        ...,
        description="Search query to find relevant documents",
        example="capital of France",
        min_length=1,
        max_length=500,
    )


class UploadRequest(BaseModel):
    """Request model for uploading and ingesting a document into the RAG system.

    Attributes:
        title (Optional[str]): Optional title for the uploaded document. If not provided, the filename will be used.
        chunk_size (int): The size of text chunks for processing. Defaults to 500.
        chunk_overlap (int): The overlap between chunks. Defaults to 50.
        min_chunk_size (int): The minimum size for a chunk. Defaults to 100.
    """

    title: Optional[str] = Field(
        None,
        description="Optional title for the uploaded document",
        example="Geography for dummies",
        max_length=200,
    )
    chunk_size: int = Field(
        500,
        description="Size of text chunks for processing",
        ge=1,
    )
    chunk_overlap: int = Field(
        50,
        description="Overlap between chunks",
        ge=0,
    )
    min_chunk_size: int = Field(
        100,
        description="Minimum size for a chunk",
        ge=1,
    )
