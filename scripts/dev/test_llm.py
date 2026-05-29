import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.llm_service import LLMService

llm_service = LLMService(system_prompt="")

context = "The capital of France is Paris. The capital of Spain is Madrid. The capital of Italy is Rome."
query = "What is the capital of France?"


async def test_llm():
    answer = await llm_service.get_answer(query=query, context=context)
    print("Answer:", answer)


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_llm())
