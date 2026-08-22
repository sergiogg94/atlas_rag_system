from pathlib import Path

import gradio as gr

from app.frontend.api_client import AtlasAPIClient
from app.frontend.components.chat import create_chat_tab
from app.frontend.components.collections import create_collections_tab
from app.frontend.components.health import create_health_tab
from app.frontend.components.ingest import create_ingest_tab
from app.frontend.components.search import create_search_tab
from app.frontend.components.upload import create_upload_tab
from app.frontend.config import (
    API_BASE_URL,
    DESCRIPTION,
    FOOTER,
    GRADIO_SERVER_NAME,
    GRADIO_SERVER_PORT,
    GRADIO_SHARE,
    THEME,
    TITLE,
)

custom_css = (Path(__file__).parent / "styles.css").read_text()


def create_app():
    # Initialize API client
    client = AtlasAPIClient(base_url=API_BASE_URL)

    # Create Gradio app
    with gr.Blocks(title=TITLE) as app:
        # Header
        with gr.Row(elem_id="header"):
            gr.Markdown(f"""
# {TITLE}
{DESCRIPTION}
            """)

        # Tabs
        with gr.Tabs():
            # Chat with RAG system
            create_chat_tab(client)

            # Manage collections
            create_collections_tab(client)

            # Ingest text
            create_ingest_tab(client)

            # Upload file
            create_upload_tab(client)

            # Search documents
            create_search_tab(client)

            # Health check
            create_health_tab(client)

        # Connect info
        with gr.Row():
            gr.Markdown(f"🔗 **API Endpoint:** `{API_BASE_URL}`")

        # Footer
        with gr.Row(elem_id="footer"):
            gr.Markdown(FOOTER)

    return app


def main():
    app = create_app()

    app.launch(
        server_name=GRADIO_SERVER_NAME,
        server_port=GRADIO_SERVER_PORT,
        share=GRADIO_SHARE,
        show_error=True,
        theme=THEME,
        css=custom_css,
    )


if __name__ == "__main__":
    main()
