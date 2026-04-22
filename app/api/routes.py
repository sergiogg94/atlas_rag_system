from fastapi import APIRouter, UploadFile, File, Form, HTTPException
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
    UploadRequest,
)
from typing import Optional

router = APIRouter()
rag_service = RAGService()


@router.get("/health")
async def health() -> dict:
    """Return a basic health status for the service.

    Returns:
        dict: A dictionary containing the current service status.
    """
    logger.info("Health check called")
    return {"status": "ok"}


@router.get("/query", response_model=QueryResponse)
async def query(payload: QueryRequest) -> QueryResponse:
    """Query the RAG service with the provided question.

    Args:
        payload (QueryRequest): The request payload containing the question to query.

    Returns:
        QueryResponse: The response from the RAG service, including the answer and source metadata.
    """
    logger.info(f"Received question: {payload.question}")
    response = await rag_service.query(payload.question)
    return QueryResponse(response=response, sources=[])


@router.post("/ingest")
async def ingest(playload: IngestRequest) -> dict:
    """Ingest a new document into the RAG system.

    Args:
        playload (IngestRequest): The request payload containing the title,
            content, and chunking parameters for the document to be ingested.

    Returns:
        dict: A dictionary containing the status of the ingestion.
    """
    logger.info("Ingest document called")
    rag_service = RAGService(
        chunk_size=playload.chunk_size,
        chunk_overlap=playload.chunk_overlap,
        min_chunk_size=playload.min_chunk_size,
    )
    await rag_service.ingest(title=playload.title, content=playload.content)
    return {"status": "ok"}


@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    chunk_size: int = Form(500),
    chunk_overlap: int = Form(50),
    min_chunk_size: int = Form(100),
) -> dict:
    """Upload and ingest a document into the RAG system.

    Args:
        file (UploadFile): The file to upload.
        title (Optional[str]): Optional title for the document.
        chunk_size (int): Size of text chunks for processing. Defaults to 500.
        chunk_overlap (int): Overlap between chunks. Defaults to 50.
        min_chunk_size (int): Minimum size for a chunk. Defaults to 100.

    Returns:
        dict: A dictionary containing the status and title of the ingested document.
    """
    logger.info(f"Upload document called with file: {file.filename}")
    try:
        upload_service = UploadService()
        return await upload_service.process_upload(
            file=file,
            title=title,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            min_chunk_size=min_chunk_size,
        )
    except DocumentValidationError as e:
        logger.error(f"Document validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except DocumentParsingError as e:
        logger.error(f"Document parsing error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except UploadProcessError as e:
        logger.error(f"Upload process error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search(payload: SearchRequest) -> dict:
    """Search for relevant documents in the RAG system based on a query.

    Args:
        payload (SearchRequest): The request payload containing the search query.

    Returns:
        dict: A dictionary containing the search results.
    """
    logger.info(f"Search called with query: {payload.query}")
    results = await rag_service.search(payload.query)
    return {"results": results}
