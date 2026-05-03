from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from app.core.logging import logger
from app.core.exceptions import (
    DocumentValidationError,
    DocumentParsingError,
    UploadProcessError,
)
from app.services.rag_service import RAGService
from app.services.upload_service import UploadService
from app.models.schemas import (
    QueryRequest,
    QueryResponse,
    IngestRequest,
    SearchRequest,
    SearchResponse,
    SearchResult,
    HealthResponse,
    ErrorResponse,
    IngestResponse,
    UploadResponse,
)
from typing import Optional
from time import perf_counter

router = APIRouter()
rag_service = RAGService()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check the health status of the Atlas API.",
)
async def health() -> HealthResponse:
    """Return a basic health status for the service."""
    logger.info("Health check called")
    return HealthResponse(
        status="ok",
        version="1.0.0",
    )


@router.get(
    "/query",
    response_model=QueryResponse,
    summary="Query the RAG system",
    description="Submit a question to the RAG system and receive an answer along with source metadata.",
    responses={
        200: {"description": "Successful response with answer."},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def query(payload: QueryRequest) -> QueryResponse:
    """Query the RAG service with the provided question."""
    logger.info(f"Received question: {payload.question}")
    response = await rag_service.query(payload.question)
    return QueryResponse(response=response, sources=[])


@router.post(
    "/ingest",
    response_model=IngestResponse,
    summary="Ingest a document into the RAG system",
    responses={
        200: {"description": "Document ingested successfully."},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def ingest(payload: IngestRequest) -> IngestResponse:
    """Ingest a new document into the RAG system.

    Args:
        payload (IngestRequest): The request payload containing the title,
            content, and chunking parameters for the document to be ingested.

    Returns:
        IngestResponse: The response containing the status of the ingestion.
    """
    logger.info("Ingest document called")
    start_time = perf_counter()

    try:
        rag_service = RAGService(
            chunk_size=payload.chunk_size,
            chunk_overlap=payload.chunk_overlap,
        )
        doc, chunk_count = await rag_service.ingest(
            title=payload.title, content=payload.content
        )

        latency_ms = round((perf_counter() - start_time) * 1000, 2)
        logger.info(f"Ingestion completed in {latency_ms} ms")

        return IngestResponse(
            document_id=doc.id,
            title=doc.title,
            chunk_count=chunk_count,
            metadata={
                "latency_ms": latency_ms,
                "chunk_size": payload.chunk_size,
                "chunk_overlap": payload.chunk_overlap,
                "content_length": len(payload.content),
            },
        )
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post(
    "/upload",
    response_model=UploadResponse,
    summary="Upload and ingest a document",
    description="Upload and process a document file (PDF, TXT, etc.)",
    responses={
        200: {"description": "File successfully uploaded and ingested"},
        400: {"model": ErrorResponse, "description": "Invalid file or parameters"},
        500: {"model": ErrorResponse, "description": "Upload processing failed"},
    },
)
async def upload(
    file: UploadFile = File(..., description="Document file to upload"),
    title: Optional[str] = Form(None, description="Optional document title"),
    chunk_size: int = Form(500, ge=100, le=2000),
    chunk_overlap: int = Form(50, ge=0, le=500),
) -> UploadResponse:
    """Upload and ingest a document into the RAG system.

    Args:
        file (UploadFile): The file to upload.
        title (Optional[str]): Optional title for the document.
        chunk_size (int): Size of text chunks for processing. Defaults to 500.
        chunk_overlap (int): Overlap between chunks. Defaults to 50.

    Returns:
        UploadResponse: The response containing the status and title of the ingested document.
    """
    logger.info(f"Upload document called with file: {file.filename}")
    start_time = perf_counter()

    try:
        upload_service = UploadService()
        doc, chunk_count, filename = await upload_service.process_upload(
            file=file,
            title=title,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        latency_ms = round((perf_counter() - start_time) * 1000, 2)
        logger.info(f"Upload and ingestion completed in {latency_ms} ms")

        return UploadResponse(
            filename=filename,
            document_id=doc.id,
            title=doc.title,
            chunk_count=chunk_count,
            metadata={
                "latency_ms": latency_ms,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
            },
        )
    except DocumentValidationError as e:
        logger.error(f"Document validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "VALIDATION_ERROR", "message": str(e)},
        )
    except DocumentParsingError as e:
        logger.error(f"Document parsing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error_code": "PARSING_ERROR", "message": str(e)},
        )
    except UploadProcessError as e:
        logger.error(f"Upload process error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error_code": "UPLOAD_ERROR", "message": str(e)},
        )


@router.post(
    "/search",
    response_model=SearchResponse,
    summary="Search documents",
    description="Search for relevant document chunks using vector similarity",
    responses={
        200: {"description": "Search results returned"},
        400: {"model": ErrorResponse, "description": "Invalid search parameters"},
        500: {"model": ErrorResponse, "description": "Search failed"},
    },
)
async def search(payload: SearchRequest) -> SearchResponse:
    """Search for relevant documents in the RAG system based on a query.

    Args:
        payload (SearchRequest): The request payload containing the search query.

    Returns:
        dict: A dictionary containing the search results.
    """
    logger.info(f"Search called with query: {payload.query}")
    start_time = perf_counter()

    try:
        results = await rag_service.search(
            query=payload.query,
            top_k=payload.top_k,
            probes=payload.probes,
            max_distance=payload.max_distance,
        )

        formatted_results = [
            SearchResult(
                document_id=result["document_id"],
                chunk_id=result["chunk_id"],
                content=result["content"],
                distance=result["distance"],
            )
            for result in results
        ]

        latency_ms = round((perf_counter() - start_time) * 1000, 2)
        logger.info(f"Search completed in {latency_ms} ms with {len(results)} results")

        return SearchResponse(
            results=formatted_results,
            total_results=len(formatted_results),
            metadata={
                "latency_ms": latency_ms,
                "top_k": payload.top_k,
                "probes": payload.probes,
                "max_distance": payload.max_distance,
            },
        )
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
