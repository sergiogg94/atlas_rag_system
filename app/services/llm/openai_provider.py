from openai import AsyncOpenAI

from app.services.llm.provider import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self, model: str, base_url: str, api_key: str):
        self.client = AsyncOpenAI(base_url=base_url, api_key=api_key)
        self.model = model

    async def get_completion(
        self, messages: list[dict], max_tokens: int = 512, temperature: float = 0.7
    ) -> str:
        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return completion.choices[0].message.content
