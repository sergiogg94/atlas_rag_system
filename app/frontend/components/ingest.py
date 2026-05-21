import asyncio
import gradio as gr

from app.frontend.api_client import AtlasAPIClient
from app.frontend.config import DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP


def create_ingest_tab(client: AtlasAPIClient):
    async def ingest_document(
        title: str,
        content: str,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    ):
        if not title or not content:
            return "⚠️ Please enter title and content", ""

        try:
            result = await client.ingest_document(
                title=title,
                content=content,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )

            status = "✅ Document ingested successfully"
            details = f"""
### Result

**Title:** {result['title']}
**Document ID:** {result['document_id']}
**Chunks created:** {result['chunk_count']}

**Metadata:**
- Latency: {result['metadata']['latency_ms']} ms
- Chunk size: {result['metadata']['chunk_size']}
- Chunk overlap: {result['metadata']['chunk_overlap']}
- Content length: {result['metadata']['content_length']} characters
            """
            return status, details

        except Exception as e:
            status = "❌ Error ingesting document"
            details = f"**Error:** {str(e)}"
            return status, details

    def sync_ingest(title, content, chunk_size, chunk_overlap):
        return asyncio.run(ingest_document(title, content, chunk_size, chunk_overlap))

    ## Start Gradio UI
    with gr.Tab("📝 Ingest Text"):
        gr.Markdown("## Ingest document from plain text input")

        with gr.Row():
            with gr.Column():
                ingest_title = gr.Textbox(
                    label="Document Title *", placeholder="Ex: SprintStep Sales Policy"
                )
                ingest_content = gr.Textbox(
                    label="Document Content *",
                    placeholder="Paste your document content here...",
                    lines=15,
                    max_lines=30,
                )

                with gr.Accordion("⚙️ Chunking Configuration", open=False):
                    ingest_chunk_size = gr.Slider(
                        label="Chunk Size",
                        minimum=100,
                        maximum=2000,
                        value=DEFAULT_CHUNK_SIZE,
                        step=50,
                        info="Size of each chunk in characters",
                    )
                    ingest_chunk_overlap = gr.Slider(
                        label="Chunk Overlap",
                        minimum=0,
                        maximum=500,
                        value=DEFAULT_CHUNK_OVERLAP,
                        step=10,
                        info="Overlap between chunks",
                    )

                ingest_btn = gr.Button("✨ Ingest Document", variant="primary")

            with gr.Column():
                ingest_status = gr.Textbox(label="Status", interactive=False)
                ingest_details = gr.Markdown()

        ingest_btn.click(
            fn=sync_ingest,
            inputs=[
                ingest_title,
                ingest_content,
                ingest_chunk_size,
                ingest_chunk_overlap,
            ],
            outputs=[ingest_status, ingest_details],
        )

        # Instructions
        gr.Markdown("""
### 📝 Instructions

1. **Title:** Descriptive name of the document
2. **Content:** Full document text
3. **Configuration:** Adjust chunking parameters as needed

**Use cases:**
- Copy/paste document content
- Ingest text without file
- Test chunks with specific content
        """)
