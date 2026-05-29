import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.rag_service import RAGService

rag_service = RAGService()

query = "What happens if my package is lost?"


async def test_search():
    resultados = await rag_service.search(
        query=query,
        top_k=5,
        max_distance=1.0,
    )

    for res in resultados:
        print(res)


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_search())
