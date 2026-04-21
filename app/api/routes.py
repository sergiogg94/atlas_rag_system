from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.core.logging import logger
from app.services.rag_service import RAGService
from app.models.schemas import (
    QueryRequest,
    QueryResponse,
    IngestRequest,
    SearchRequest,
    UploadRequest,
)
from app.services.validators import validate_document
from app.services.parsers import DocumentParser
from pathlib import Path
import tempfile
import os
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
        playload (IngestRequest): The request payload containing the title
            and content of the document to be ingested.

    Returns:
        dict: A dictionary containing the status of the ingestion.
    """
    logger.info("Ingest document called")
    await rag_service.ingest(title=playload.title, content=playload.content)
    return {"status": "ok"}


@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
) -> dict:
    logger.info(f"Upload document called with file: {file.filename}")

    # Validate input using UploadRequest schema
    upload_request = UploadRequest(title=title)

    # Create a temporary directory and save the file
    temp_dir = tempfile.gettempdir()
    file_path = Path(temp_dir) / file.filename

    try:
        # Save the uploaded file to the temporary directory
        logger.info(f"Saving file to temporary location: {file_path}")
        with open(file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)

        # Validate the document
        is_valid, error_message = validate_document(file_path)
        if not is_valid:
            logger.error(f"Document validation failed: {error_message}")
            raise HTTPException(status_code=400, detail=error_message)

        # Parse the document
        parser = DocumentParser()
        parsed_content = parser.parse(file_path)
        if parsed_content is None:
            logger.error("Failed to parse document")
            raise HTTPException(status_code=400, detail="Failed to parse the document.")

        # Use provided title or fall back to filename
        document_title = upload_request.title or file.filename

        # Ingest the parsed content
        await rag_service.ingest(title=document_title, content=parsed_content)

        logger.info(f"Document '{document_title}' uploaded and ingested successfully.")
        return {"status": "ok", "title": document_title}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during document upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Clean up the temporary file
        if file_path.exists():
            try:
                os.remove(file_path)
                logger.info(f"Temporary file removed: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to remove temporary file {file_path}: {e}")


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
