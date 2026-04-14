from fastapi import APIRouter
from app.core.logging import logger
from app.services.rag_service import RAGService
from app.models.schemas import QueryRequest, QueryResponse

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
