import asyncio
import gradio as gr
from typing import List

from app.frontend.api_client import AtlasAPIClient
from app.frontend.config import DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP


def create_upload_tab(client: AtlasAPIClient):
    async def upload_document(
        file_path: str,
        title: str,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    ):
        if not file_path:
            return "⚠️ Please select a file to upload", ""

        try:
            result = await client.upload_document(
                file_path=file_path,
                title=title,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )

            status = "✅ Document uploaded and ingested successfully"
            details = f"""
### Result

**File:** {result['filename']}
**Title:** {result['title']}
**Document ID:** {result['document_id']}
**Chunks created:** {result['chunk_count']}

**Metadata:**
- Latency: {result['metadata']['latency_ms']} ms
- Chunk size: {result['metadata']['chunk_size']}
- Chunk overlap: {result['metadata']['chunk_overlap']}
            """
            return status, details

        except Exception as e:
            status = "❌ Error uploading document"
            details = f"**Error:** {str(e)}"
            return status, details

    async def upload_batch(
        file_paths: List[str],
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        if not file_paths:
            return "⚠️ Please select at least one file to upload", ""

        try:
            results = await client.upload_batch(
                file_paths=file_paths,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )

            status = "✅ Batch upload completed"
            details = "### Results\n\n"
            for result in results:
                if result["status"] == "success":
                    details += f"""**File:** {result['file']}
**Title:** {result['data']['title']}
**Document ID:** {result['data']['document_id']}
**Chunks created:** {result['data']['chunk_count']}

**Metadata:**
- Latency: {result['data']['metadata']['latency_ms']} ms
- Chunk size: {result['data']['metadata']['chunk_size']}
- Chunk overlap: {result['data']['metadata']['chunk_overlap']}

---
"""
                else:
                    details += f"""**File:** {result['file']}
**Error:** {result['error']}
"""
                details += "\n---\n"

            return status, details

        except Exception as e:
            status = "❌ Error during batch upload"
            details = f"**Error:** {str(e)}"
            return status, details

    def sync_upload(file_path, title, chunk_size, chunk_overlap):
        return asyncio.run(upload_document(file_path, title, chunk_size, chunk_overlap))

    def sync_upload_batch(file_paths, chunk_size, chunk_overlap):
        return asyncio.run(upload_batch(file_paths, chunk_size, chunk_overlap))

    ## Start Gradio UI
    with gr.Tab("📁 Upload Documents"):
        gr.Markdown("## Upload and ingest document files (PDF, TXT, MD)")

        with gr.Tabs():
            # Individual file upload
            with gr.Tab("Single Upload"):
                with gr.Row():
                    with gr.Column():
                        upload_file = gr.File(
                            label="Select a document file to upload",
                            file_types=[".pdf", ".txt", ".md"],
                        )
                        upload_title = gr.Textbox(
                            label="Optional Document Title",
                            placeholder="Ex: SprintStep Sales Policy",
                        )

                        with gr.Accordion("⚙️ Advanced Configuration", open=False):
                            upload_chunk_size = gr.Slider(
                                label="Chunk Size",
                                minimum=100,
                                maximum=2000,
                                value=DEFAULT_CHUNK_SIZE,
                                step=50,
                            )
                            upload_chunk_overlap = gr.Slider(
                                label="Chunk Overlap",
                                minimum=0,
                                maximum=500,
                                value=DEFAULT_CHUNK_OVERLAP,
                                step=10,
                            )

                        upload_btn = gr.Button("📤 Upload file", variant="primary")

                    with gr.Column():
                        upload_status = gr.Textbox(label="Status", interactive=False)
                        upload_details = gr.Markdown()

                upload_btn.click(
                    fn=sync_upload,
                    inputs=[
                        upload_file,
                        upload_title,
                        upload_chunk_size,
                        upload_chunk_overlap,
                    ],
                    outputs=[upload_status, upload_details],
                )

            # Multiple file upload
            with gr.Tab("Batch Upload"):
                with gr.Row():
                    with gr.Column():
                        batch_files = gr.File(
                            label="Select multiple document files for batch upload",
                            file_types=[".pdf", ".txt", ".md"],
                            file_count="multiple",
                        )

                        with gr.Accordion("⚙️ Advanced Configuration", open=False):
                            batch_chunk_size = gr.Slider(
                                label="Chunk Size",
                                minimum=100,
                                maximum=2000,
                                value=DEFAULT_CHUNK_SIZE,
                                step=50,
                            )
                            batch_chunk_overlap = gr.Slider(
                                label="Chunk Overlap",
                                minimum=0,
                                maximum=500,
                                value=DEFAULT_CHUNK_OVERLAP,
                                step=10,
                            )

                        batch_upload_btn = gr.Button(
                            "📤 Upload Batch", variant="primary"
                        )

                    with gr.Column():
                        batch_upload_status = gr.Textbox(
                            label="Status", interactive=False
                        )
                        batch_upload_details = gr.Markdown()

                batch_upload_btn.click(
                    fn=sync_upload_batch,
                    inputs=[batch_files, batch_chunk_size, batch_chunk_overlap],
                    outputs=[batch_upload_status, batch_upload_details],
                )

        # Instructions
        gr.Markdown("""
### 📝 Instructions

**Single Upload:**
1. Select a file (PDF, TXT, MD)
2. (Optional) Specify a title
3. Adjust chunking parameters if necessary
4. Click "Upload Document"

**Batch Upload:**
1. Select multiple files
2. Adjust chunking parameters (applied to all)
3. Click "Upload Batch"

**Supported Formats:** PDF, TXT, Markdown
        """)
