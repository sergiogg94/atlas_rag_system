from voyageai import AsyncClient
from app.core.config import settings
from typing import List


class EmbeddingsService:
    """Service for generating embeddings using the Voyage API."""

    # TODO: Implement also a version with OpenAI's embedding models and look up for more embedding models in the future, e.g. from Hugging Face.
    def __init__(self):
        self.client = AsyncClient(api_key=settings.voyage_api_key)
        self.model = "voyage-4-lite"
        self.embedding_dimension = 256

    async def encode(self, texts: List[str]) -> List[List[float]] | List[List[int]]:
        """Generates embeddings for the given texts.

        Args:
            texts (_type_): _description_

        Returns:
            _type_: _description_
        """
        result = await self.client.embed(
            texts=texts,
            model=self.model,
            output_dimension=self.embedding_dimension,
        )

        return result.embeddings
