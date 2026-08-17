from app.core.config import settings
from app.services.embeddings.local_provider import LocalProvider
from app.services.embeddings.provider import EmbeddingProvider
from app.services.embeddings.voyage_provider import VoyageProvider

PROVIDER_CATALOG: dict[str, dict] = {
    "voyage": {
        "models": {
            "voyage-3-lite": {
                "default_dimension": 512,
                "supports_matryoshka": True,
                "min_dim": 512,
                "max_dim": 512,
            },
            "voyage-3": {
                "default_dimension": 1024,
                "supports_matryoshka": True,
                "min_dim": 256,
                "max_dim": 1024,
            },
            "voyage-4": {
                "default_dimension": 1024,
                "supports_matryoshka": True,
                "min_dim": 256,
                "max_dim": 2048,
            },
        }
    },
    "local": {
        "models": {
            "sentence-transformers/all-MiniLM-L6-v2": {
                "default_dimension": 384,
                "supports_matryoshka": False,
            },
            "sentence-transformers/all-mpnet-base-v2": {
                "default_dimension": 768,
                "supports_matryoshka": False,
            },
            "BAAI/bge-small-en-v1.5": {
                "default_dimension": 384,
                "supports_matryoshka": False,
            },
        }
    },
}


def get_provider_catalog() -> dict:
    return PROVIDER_CATALOG


def get_embedding_provider(
    provider: str, model: str, dimension: int
) -> EmbeddingProvider:
    provider_name = provider.lower()

    if provider_name == "voyage":
        return VoyageProvider(
            api_key=settings.voyage_api_key,
            model=model,
            dimension=dimension,
        )
    elif provider_name == "local":
        return LocalProvider(
            model_name=model,
            dimension=dimension,
        )
    else:
        raise ValueError(f"Unsupported embedding provider: {provider_name}")
