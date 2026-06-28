import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration loaded from environment variables.

    This class reads environment variables for the application environment.
    """

    def __init__(self):
        # Basic settings
        self.app_env = os.getenv("APP_ENV", "dev")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

        # Database settings
        self.database_url = os.getenv("DATABASE_URL")

        # API key's
        self.voyage_api_key = os.getenv("VOYAGE_API_KEY")
        self.hf_token = os.getenv("HF_TOKEN")

        # Embedding provider settings
        self.embedding_provider = os.getenv("EMBEDDING_PROVIDER", "voyage")
        self.voyage_model = os.getenv("VOYAGE_MODEL", "voyage-4")
        self.voyage_embedding_dimension = int(
            os.getenv("VOYAGE_EMBEDDING_DIMENSION", "1024")
        )

        # LLM provider settings
        self.llm_provider = os.getenv("LLM_PROVIDER", "groq")

        # OpenAI-compatible provider (includes HuggingFace, Groq, etc.)
        self.openai_base_url = os.getenv(
            "OPENAI_BASE_URL", "https://router.huggingface.co/v1"
        )
        self.openai_model = os.getenv(
            "OPENAI_MODEL", "katanemo/Arch-Router-1.5B:hf-inference"
        )

        # Groq (uses OpenAI-compatible API)
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.groq_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

        # API settings
        self.api_base_url = os.path.expandvars(
            os.getenv("API_BASE_URL", "http://localhost:8000")
        )

        # Gradio settings
        self.gradio_server_name = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
        self.gradio_server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
        self.gradio_share = os.getenv("GRADIO_SHARE", "False").lower() in (
            "true",
            "1",
            "t",
        )


settings = Settings()
