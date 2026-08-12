import asyncio
import threading

from app.core.logging import logger
from app.services.embeddings.provider import EmbeddingProvider


class LocalProvider(EmbeddingProvider):
    """Sentence Transformers provider running a local HuggingFace model."""

    def __init__(self, model_name: str, dimension: int | None = None):
        self.model_name = model_name
        self._dimension = dimension
        self._model = None
        self._lock = threading.Lock()

    @property
    def embedding_dimension(self) -> int:
        if self._dimension is not None:
            return self._dimension
        if self._model is not None:
            return self._model.get_embedding_dimension()
        raise ValueError(
            "Local embedding dimension is not configured and the model "
            "has not been loaded yet"
        )

    def _get_model(self):
        with self._lock:
            if self._model is None:
                from sentence_transformers import SentenceTransformer

                logger.info("Loading local embedding model: %s", self.model_name)
                self._model = SentenceTransformer(self.model_name)
                model_dim = self._model.get_embedding_dimension()
                if self._dimension is not None and model_dim != self._dimension:
                    logger.warning(
                        "Local embedding model '%s' outputs %d dimensions "
                        "but %d is configured",
                        self.model_name,
                        model_dim,
                        self._dimension,
                    )
                logger.info("Local embedding model loaded successfully")
        return self._model

    async def encode(self, texts: list[str]) -> list[list[float]]:
        model = await asyncio.to_thread(self._get_model)
        embeddings = await asyncio.to_thread(
            model.encode, texts, normalize_embeddings=True
        )
        return embeddings.tolist()
