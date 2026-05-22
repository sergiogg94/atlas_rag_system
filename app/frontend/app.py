import gradio as gr

from app.frontend.api_client import AtlasAPIClient
from app.frontend.config import (
    API_BASE_URL,
    GRADIO_SERVER_NAME,
    GRADIO_SERVER_PORT,
    GRADIO_SHARE,
    THEME,
    TITLE,
    DESCRIPTION,
)
from app.frontend.components.ingest import create_ingest_tab
from app.frontend.components.upload import create_upload_tab
from app.frontend.components.health import create_health_tab

custom_css = """
#header {
    text-align: center;
    padding: 20px;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    margin-bottom: 20px;
}

#footer {
    text-align: center;
    padding: 15px;
    color: #666;
    margin-top: 30px;
    border-top: 1px solid #ddd;
}

.gradio-container {
    max-width: 1400px !important;
}

.tab-nav button {
    font-size: 16px !important;
    font-weight: 500 !important;
}
"""


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

        # Connect info
        with gr.Row():
            gr.Markdown(f"🔗 **API Endpoint:** `{API_BASE_URL}`")

        # Tabs
        with gr.Tabs():
            # Ingest text
            create_ingest_tab(client)

            # Upload file
            create_upload_tab(client)

            # Health check
            create_health_tab(client)

        # Footer
        with gr.Row(elem_id="footer"):
            gr.Markdown("""
---
**Atlas RAG System** v1.0 | Developed with FastAPI + Gradio + PostgreSQL + pgvector  
📚 [Documentation](https://github.com/sergiogg94/atlas_rag_system) | 
🐛 [Report Bug](https://github.com/sergiogg94/atlas_rag_system/issues)
            """)

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
