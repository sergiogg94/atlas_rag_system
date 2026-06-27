from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    async def get_completion(
        self, messages: list[dict], max_tokens: int = 512, temperature: float = 0.7
    ) -> str: ...
