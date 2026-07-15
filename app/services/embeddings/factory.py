from app.core.config import settings
from app.services.embeddings.voyage_provider import VoyageProvider

_providers: dict[str, type[VoyageProvider]] = {
    "voyage": VoyageProvider,
}


def get_embedding_provider() -> VoyageProvider:
    provider_name = settings.embedding_provider.lower()

    cls = _providers.get(provider_name)
    if provider_name == "voyage":
        return cls(
            api_key=settings.voyage_api_key,
            model=settings.voyage_model,
            dimension=settings.voyage_embedding_dimension,
        )
    else:
        raise ValueError(f"Unsupported embedding provider: {provider_name}")
