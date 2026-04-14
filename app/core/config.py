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


settings = Settings()
