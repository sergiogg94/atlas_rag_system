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
        self.postgres_user = os.getenv("POSTGRES_USER")
        self.postgres_password = os.getenv("POSTGRES_PASSWORD")
        self.postgres_db = os.getenv("POSTGRES_DB")
        self.postgres_host = os.getenv("POSTGRES_HOST", "localhost")
        self.postgres_port = os.getenv("POSTGRES_PORT", "5432")

        # API key's
        self.voyage_api_key = os.getenv("VOYAGE_API_KEY")
        self.hf_token = os.getenv("HF_TOKEN")

        # API settings
        self.api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")

        # Gradio settings
        self.gradio_server_name = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
        self.gradio_server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
        self.gradio_share = os.getenv("GRADIO_SHARE", "False").lower() in (
            "true",
            "1",
            "t",
        )


settings = Settings()
