from fastapi import APIRouter
from app.core.logging import logger
from app.services.rag_service import RAGService
from app.models.schemas import QueryRequest, QueryResponse

router = APIRouter()
rag_service = RAGService()


@router.get("/health")
async def health():
    logger.info("Health check called")
    return {"status": "ok"}


@router.get("/query", response_model=QueryResponse)
async def query(payload: QueryRequest):
    logger.info(f"Received query: {payload.question}")
    response = await rag_service.query(payload.question)
    return QueryResponse(response=response, sources=[])
