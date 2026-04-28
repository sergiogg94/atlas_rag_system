from pydantic import BaseModel, Field
from typing import Optional


class QueryRequest(BaseModel):
    """Request model for a question to query the RAG service."""

    question: str = Field(
        ...,
        description="User question to be processed",
        example="What is the capital of France?",
        min_length=1,
        max_length=500,
    )


class QueryResponse(BaseModel):
    """Response model returned by the RAG service."""

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
    """Request model for ingesting a new document into the RAG system."""

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
    """Request model for searching documents in the RAG system."""

    query: str = Field(
        ...,
        description="Search query to find relevant documents",
        example="capital of France",
        min_length=1,
        max_length=500,
    )

    top_k: int = Field(
        5,
        description="Number of top matching chunks to return",
        ge=1,
        le=100,
    )

    probes: int = Field(
        10,
        description="Number of probes to use for the search",
        ge=1,
        le=100,
    )

    max_distance: float = Field(
        0.5,
        description="Maximum cosine distance for a chunk to be considered a match",
        ge=0.0,
        le=1.0,
    )


class UploadRequest(BaseModel):
    """Request model for uploading and ingesting a document into the RAG system."""

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
