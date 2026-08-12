from app.core.config import settings
from app.services.embeddings.local_provider import LocalProvider
from app.services.embeddings.provider import EmbeddingProvider
from app.services.embeddings.voyage_provider import VoyageProvider

_providers: dict[str, type[EmbeddingProvider]] = {
    "voyage": VoyageProvider,
    "local": LocalProvider,
}


def get_embedding_provider() -> EmbeddingProvider:
    provider_name = settings.embedding_provider.lower()

    cls = _providers.get(provider_name)
    if provider_name == "voyage":
        return cls(
            api_key=settings.voyage_api_key,
            model=settings.voyage_model,
            dimension=settings.voyage_embedding_dimension,
        )
    elif provider_name == "local":
        return cls(
            model_name=settings.local_embedding_model,
            dimension=settings.local_embedding_dimension,
        )
    else:
        raise ValueError(f"Unsupported embedding provider: {provider_name}")
