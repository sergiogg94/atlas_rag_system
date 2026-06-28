from typing import List

from app.services.embeddings.provider import EmbeddingProvider


class EmbeddingsService:
    def __init__(self, provider: EmbeddingProvider):
        self.provider = provider

    @property
    def embedding_dimension(self) -> int:
        return self.provider.embedding_dimension

    async def encode(self, texts: List[str]) -> List[List[float]]:
        return await self.provider.encode(texts)
