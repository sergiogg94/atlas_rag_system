import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.services.llm_service import LLMService
from app.services.llm.openai_provider import OpenAIProvider

if settings.llm_provider == "groq":
    provider = OpenAIProvider(
        model=settings.groq_model,
        base_url="https://api.groq.com/openai/v1",
        api_key=settings.groq_api_key,
    )
else:
    provider = OpenAIProvider(
        model=settings.openai_model,
        base_url=settings.openai_base_url,
        api_key=settings.hf_token,
    )

llm_service = LLMService(provider=provider, system_prompt="")

context = "The capital of France is Paris. The capital of Spain is Madrid. The capital of Italy is Rome."
query = "What is the capital of France?"


async def test_llm():
    answer = await llm_service.get_answer(query=query, context=context)
    print("Answer:", answer)


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_llm())
