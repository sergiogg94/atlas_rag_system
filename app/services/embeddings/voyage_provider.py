from typing import List

from voyageai import AsyncClient

from app.services.embeddings.provider import EmbeddingProvider


class VoyageProvider(EmbeddingProvider):
    def __init__(self, api_key: str, model: str = "voyage-4", dimension: int = 1024):
        self.client = AsyncClient(api_key=api_key)
        self.model = model
        self._dimension = dimension

    @property
    def embedding_dimension(self) -> int:
        return self._dimension

    async def encode(self, texts: List[str]) -> List[List[float]]:
        result = await self.client.embed(
            texts=texts,
            model=self.model,
            output_dimension=self._dimension,
        )
        return result.embeddings
