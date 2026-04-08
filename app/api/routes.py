from fastapi import APIRouter
from app.core.logging import logger

router = APIRouter()


@router.get("/health")
async def health():
    logger.info("Health check called")
    return {"status": "ok"}


@router.get("/query")
async def query(payload: dict):
    return {"message": "Not implemented yet"}
