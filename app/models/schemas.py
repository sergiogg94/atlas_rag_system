from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


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
    error_code: str = Field(
        ..., description="Error code", examples=["VALIDATION_ERROR"]
    )
    message: str = Field(..., description="Error message", examples=["Invalid input"])
    details: dict | None = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


## Health
class HealthResponse(BaseResponse):
    """Response model for the health check endpoint."""

    service: str = Field("Atlas API", description="Service name")
    version: str = Field("1.0.0", description="Service version")


## Query
class QueryRequest(BaseModel):
    """Request model for a question to query the RAG service."""

    collection_id: int = Field(..., description="ID of collection to query")

    question: str = Field(
        ...,
        description="User question to be processed",
        examples=["What is the capital of France?"],
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

    temperature: float = Field(
        0.7,
        description="Temperature for LLM response generation (0.0 to 1.0)",
        ge=0.0,
        le=1.0,
    )

    max_tokens: int = Field(
        512,
        description="Maximum number of tokens for the LLM response",
        ge=1,
        le=2048,
    )


class SourceReference(BaseModel):
    """Reference to a source chunk used in the answer."""

    chunk_id: int = Field(..., description="ID of the chunk")
    document_id: int = Field(..., description="ID of the document")
    document_title: str = Field(..., description="Title of the document")
    distance: float = Field(..., description="Cosine distance (relevance score)")
    content: str | None = Field(
        None,
        description="Excerpt of the chunk content",  # , max_length=200
    )


class QueryResponse(BaseResponseWithMetadata):
    """Response model returned by the RAG service."""

    response: str = Field(
        ...,
        description="Answer generated",
        examples=["The capital of France is Paris."],
    )
    sources: list[SourceReference] = Field(
        [],
        description="List of sources used to generate the answer",
    )


## Ingest
class IngestRequest(BaseModel):
    """Request model for ingesting a new document into the RAG system."""

    title: str = Field(
        ...,
        description="Title of the document to be ingested",
        examples=["Geography for dummies"],
        min_length=1,
        max_length=200,
    )
    content: str = Field(
        ...,
        description="Content of the document to be ingested",
        examples=["France is a country in Europe. The capital of France is Paris."],
        min_length=1,
    )
    collection_id: int = Field(..., description="ID of the destination collection")
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


class IngestResponse(BaseResponseWithMetadata):
    """Response model for the ingest endpoint."""

    document_id: int = Field(..., description="ID of the ingested document")
    title: str = Field(
        ...,
        description="Title of the ingested document",
        examples=["Geography for dummies"],
    )
    chunk_count: int = Field(..., description="Number of chunks created")


## Upload
class UploadResponse(IngestResponse):
    """Response model for the upload endpoint."""

    filename: str = Field(
        ..., description="Name of the uploaded file", examples=["geography.pdf"]
    )


## Search
class SearchRequest(BaseModel):
    """Request model for searching documents in the RAG system."""

    collection_id: int = Field(..., description="ID of the collection to search")

    query: str = Field(
        ...,
        description="Search query to find relevant documents",
        examples=["capital of France"],
        min_length=1,
        max_length=500,
    )

    top_k: int = Field(
        5,
        description="Number of top matching chunks to return",
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


## Collections
class CollectionCreate(BaseModel):
    """Request for creating a new collection"""

    name: str = Field(
        ..., min_length=1, max_length=100, examples=["documentos-legales"]
    )
    description: str | None = Field(None, max_length=500)
    provider: str = Field(..., examples=["voyage"])
    model: str = Field(..., examples=["voyage-3-lite"])
    dimension: int = Field(..., ge=64, le=4096, examples=[512])


class CollectionResponse(BaseResponse):
    """Respuesta model with collection detail."""

    id: int
    name: str
    description: str | None
    provider: str
    model: str
    dimension: int
    created_at: datetime


class CollectionListResponse(BaseResponse):
    """List of available collections."""

    collections: list[CollectionResponse]
    total: int
