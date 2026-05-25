import asyncio
import gradio as gr

from app.frontend.api_client import AtlasAPIClient
from app.frontend.config import (
    DEFAULT_TOP_K,
    DEFAULT_MAX_DISTANCE,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
)


def create_chat_tab(client: AtlasAPIClient):
    async def chat(
        query: str,
        top_k: int = DEFAULT_TOP_K,
        max_distance: float = DEFAULT_MAX_DISTANCE,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        history: list = [],
    ):
        if not query:
            return history, "", "⚠️ Please enter a question to chat with", ""

        try:
            result = await client.query(
                query=query,
                top_k=top_k,
                max_distance=max_distance,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            history.append((query, result["response"]))

            # Construct sources details
            sources_md = "### 📚 Source References\n\n"
            for i, src in enumerate(result["sources"], start=1):
                sources_md += f"""
**Source {i}:** {src['document_title']}
- **Document ID:** {src['document_id']}
- **Chunk ID:** {src['chunk_id']}
- **Relevance Score:** {1 - src['distance']:.2f}
- **Content:** {src['content']}
---
                """

            # Construct metadata details
            metadata_md = f"""
**Metadata:**
- Latency: {result['metadata']['latency_ms']} ms
            """

            return history, "", metadata_md, sources_md

        except Exception as e:
            status = f"❌ Error during chat query\n**Error:** {str(e)}"
            return history, query, status, ""

    def sync_chat(query, top_k, max_distance, temperature, max_tokens, history):
        return asyncio.run(
            chat(
                query=query,
                top_k=top_k,
                max_distance=max_distance,
                temperature=temperature,
                max_tokens=max_tokens,
                history=history,
            )
        )

    ## Start Gradio UI
    with gr.Tab("💬 Chat with RAG"):
        gr.Markdown("## Ask questions and get answers with source references")

        with gr.Row():
            with gr.Column(scale=2):
                chatbot = gr.Chatbot(label="Conversation", height=500, buttons=["copy"])

                with gr.Row():
                    question_input = gr.Textbox(
                        label="Your question",
                        placeholder="¿What is the capital of France?",
                        lines=2,
                        scale=4,
                    )
                    submit_btn = gr.Button("Submint", variant="primary", scale=1)

                clear_btn = gr.Button("🗑️ Clear Chat")

            with gr.Column(scale=1):
                with gr.Accordion("⚙️ Advanced Configuration", open=True):
                    top_k_slider = gr.Slider(
                        label="Top K",
                        minimum=1,
                        maximum=20,
                        value=DEFAULT_TOP_K,
                        step=1,
                        info="Number of chunks to retrieve",
                    )
                    max_distance_slider = gr.Slider(
                        label="Max Distance",
                        minimum=0.0,
                        maximum=2.0,
                        value=DEFAULT_MAX_DISTANCE,
                        step=0.1,
                        info="Maximum similarity distance",
                    )
                    temperature_slider = gr.Slider(
                        label="Temperature",
                        minimum=0.0,
                        maximum=1.0,
                        value=DEFAULT_TEMPERATURE,
                        step=0.1,
                        info="LLM creativity level",
                    )
                    max_tokens_slider = gr.Slider(
                        label="Max Tokens",
                        minimum=128,
                        maximum=2048,
                        value=DEFAULT_MAX_TOKENS,
                        step=128,
                        info="Maximum response length",
                    )

                metadata_output = gr.Markdown(label="Metadata")

        with gr.Row():
            sources_output = gr.Markdown(label="Sources")

        # Event handlers
        submit_btn.click(
            fn=sync_chat,
            inputs=[
                question_input,
                top_k_slider,
                max_distance_slider,
                temperature_slider,
                max_tokens_slider,
                chatbot,
            ],
            outputs=[chatbot, question_input, metadata_output, sources_output],
        )

        question_input.submit(
            fn=sync_chat,
            inputs=[
                question_input,
                top_k_slider,
                max_distance_slider,
                temperature_slider,
                max_tokens_slider,
                chatbot,
            ],
            outputs=[chatbot, question_input, metadata_output, sources_output],
        )

        clear_btn.click(
            fn=lambda: ([], "", ""), outputs=[chatbot, metadata_output, sources_output]
        )
