from fastapi import APIRouter
from app.core.logging import logger
from app.services.rag_service import RAGService
from app.models.schemas import QueryRequest, QueryResponse, IngestRequest, SearchRequest

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
    logger.info(f"Received query: {payload.question}")
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
    await rag_service.ingest(title=playload.title, content=playload.content)
    return {"status": "ok"}


@router.get("/search")
async def search(payload: SearchRequest) -> dict:
    """Search for relevant documents in the RAG system based on a query.

    Args:
        payload (SearchRequest): The request payload containing the search query.

    Returns:
        dict: A dictionary containing the search results.
    """
    results = await rag_service.search(payload.query)
    return {"results": results}
