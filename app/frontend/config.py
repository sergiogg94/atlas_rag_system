from app.core.config import settings

# API configuration
API_BASE_URL = settings.api_base_url

# Gradio configuration
GRADIO_SERVER_NAME = settings.gradio_server_name
GRADIO_SERVER_PORT = settings.gradio_server_port
GRADIO_SHARE = settings.gradio_share

# Default Parameters
DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 50
DEFAULT_TOP_K = 5
DEFAULT_MAX_DISTANCE = 1.0
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 512
DEFAULT_PROBES = 10

# UI Configuration
THEME = "soft"
TITLE = "Atlas RAG System"
DESCRIPTION = """
🚀 **RAG System for document management**

Upload documents, ingest them into the vector database, and chat with your knowledge.
"""
