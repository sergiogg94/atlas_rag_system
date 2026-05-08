import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.rag_service import RAGService

rag_service = RAGService()


async def test_query():
    question = "What happens if my package is lost?"
    answer = await rag_service.query(question)
    print("Answer:", answer)


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_query())
