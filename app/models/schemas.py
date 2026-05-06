from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


## Base models
class BaseResponse(BaseModel):
    """Base model response for all API endpoints."""

    status: str = Field("success", description="Status of the API response")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Response timestamp"
    )


class BaseResponseWithMetadata(BaseResponse):
    """Base response model that includes a data field for successful responses."""

    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class ErrorResponse(BaseModel):
    """Model for error responses."""

    status: str = Field(default="error", description="Response status")
    error_code: str = Field(..., description="Error code", example="VALIDATION_ERROR")
    message: str = Field(..., description="Error message", example="Invalid input")
    details: Optional[dict] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


## Health
class HealthResponse(BaseResponse):
    """Response model for the health check endpoint."""

    service: str = Field("Atlas API", description="Service name")
    version: str = Field("1.0.0", description="Service version")


## Query
class QueryRequest(BaseModel):
    """Request model for a question to query the RAG service."""

    question: str = Field(
        ...,
        description="User question to be processed",
        example="What is the capital of France?",
        min_length=1,
        max_length=500,
    )


class QueryResponse(BaseResponse):
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


## Ingest
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


class IngestResponse(BaseResponseWithMetadata):
    """Response model for the ingest endpoint."""

    document_id: int = Field(..., description="ID of the ingested document")
    title: str = Field(
        ...,
        description="Title of the ingested document",
        example="Geography for dummies",
    )
    chunk_count: int = Field(..., description="Number of chunks created")


## Upload
class UploadResponse(IngestResponse):
    """Response model for the upload endpoint."""

    filename: str = Field(
        ..., description="Name of the uploaded file", example="geography.pdf"
    )


## Search
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
        1.0,
        description="Maximum cosine distance for a chunk to be considered a match",
        ge=0.0,
        le=1.0,
    )


class SearchResult(BaseModel):
    """Individual search result."""

    document_id: int = Field(..., description="Document ID")
    chunk_id: int = Field(..., description="Chunk ID")
    content: str = Field(..., description="Chunk content")
    distance: float = Field(..., description="Cosine distance from query")


class SearchResponse(BaseResponseWithMetadata):
    """Response model for search endpoint."""

    results: list[SearchResult] = Field(
        default_factory=list, description="List of matching chunks"
    )
    total_results: int = Field(..., description="Number of results returned")
