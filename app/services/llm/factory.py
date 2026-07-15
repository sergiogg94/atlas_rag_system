from app.core.config import settings
from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.provider import LLMProvider

_providers: dict[str, type[LLMProvider]] = {
    "openai": OpenAIProvider,
    "groq": OpenAIProvider,
}


def get_llm_provider() -> LLMProvider:
    provider_name = settings.llm_provider.lower()

    cls = _providers.get(provider_name)
    if provider_name == "groq":
        return cls(
            model=settings.groq_model,
            base_url="https://api.groq.com/openai/v1",
            api_key=settings.groq_api_key,
        )
    elif provider_name == "openai":
        return cls(
            model=settings.openai_model,
            base_url=settings.openai_base_url,
            api_key=settings.hf_token,
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider_name}")
