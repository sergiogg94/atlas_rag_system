from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):
    @property
    @abstractmethod
    def embedding_dimension(self) -> int: ...

    @abstractmethod
    async def encode(self, texts: List[str]) -> List[List[float]]: ...
