import asyncio
import gradio as gr

from app.frontend.api_client import AtlasAPIClient
from app.frontend.config import DEFAULT_TOP_K, DEFAULT_PROBES, DEFAULT_MAX_DISTANCE


def create_seach_tab(client: AtlasAPIClient):
    async def search(
        query: str,
        top_k: int = DEFAULT_TOP_K,
        probes: int = DEFAULT_PROBES,
        max_distance: float = DEFAULT_MAX_DISTANCE,
    ):
        if not query:
            return "⚠️ Please enter a search query", ""

        try:
            result = await client.search(
                query=query,
                top_k=top_k,
                probes=probes,
                max_distance=max_distance,
            )
            total = result.get("total_results", 0)

            # Not results found case
            if total == 0:
                status = "🔍 No relevant documents found"
                details = (
                    "Try adjusting your query or search parameters for better results."
                )
                return status, details, 0

            # Construct results details
            status = f"✅ Found {total} relevant chunks"

            details = "### 📄 Top Search Results\n\n"
            for i, res in enumerate(result["results"], start=1):
                similarity = 1 - res["distance"]
                sim_emoji = (
                    "🟢" if similarity > 0.8 else "🟡" if similarity > 0.5 else "🔴"
                )

                details += f"""
#### {sim_emoji} Result {i}
**Document ID:** {res['document_id']}
**Chunk ID:** {res['chunk_id']}
**Similarity:** {similarity:.2f}

**Content:** 
{res['content']}

---
                """

            details += f"""
### Metadata
- Latency: {result['metadata']['latency_ms']} ms
- Top K: {result['metadata']['top_k']}
- Probes: {result['metadata']['probes']}
- Max Distance: {result['metadata']['max_distance']}
"""
            return status, details, total

        except Exception as e:
            status = "❌ Error performing search"
            details = f"**Error:** {str(e)}"
            return status, details, 0

    def sync_search(
        query: str,
        top_k: int = DEFAULT_TOP_K,
        probes: int = DEFAULT_PROBES,
        max_distance: float = DEFAULT_MAX_DISTANCE,
    ):
        return asyncio.run(search(query, top_k, probes, max_distance))

    ## Start Gradio UI
    with gr.Tab("🔍 Search"):
        gr.Markdown("## Search for relevant documents")

        with gr.Row():
            with gr.Column(scale=2):
                query_input = gr.Textbox(
                    label="Search Query",
                    placeholder="Enter your search query here...",
                    lines=2,
                )
                search_btn = gr.Button("🔎 Search", variant="primary")

                with gr.Row():
                    search_status = gr.Textbox(
                        label="Status", interactive=False, scale=3
                    )
                    results_count = gr.Number(
                        label="Results", interactive=False, scale=1
                    )

            with gr.Column(scale=1):
                with gr.Accordion("⚙️ Search Parameters", open=False):
                    top_k_input = gr.Slider(
                        label="Top K",
                        minimum=1,
                        maximum=20,
                        value=DEFAULT_TOP_K,
                        step=1,
                    )
                    probes_input = gr.Slider(
                        label="Probes",
                        minimum=1,
                        maximum=50,
                        value=DEFAULT_PROBES,
                        step=1,
                    )
                    max_distance_input = gr.Slider(
                        label="Max Distance",
                        minimum=0.0,
                        maximum=1.0,
                        value=DEFAULT_MAX_DISTANCE,
                        step=0.01,
                    )

        with gr.Row():
            search_results = gr.Markdown(label="Search Results")

        # Event handlers
        search_btn.click(
            fn=sync_search,
            inputs=[query_input, top_k_input, probes_input, max_distance_input],
            outputs=[search_status, search_results, results_count],
        )

        query_input.submit(
            fn=sync_search,
            inputs=[query_input, top_k_input, probes_input, max_distance_input],
            outputs=[search_status, search_results, results_count],
        )

        # Instructions
        gr.Markdown("""
### 📝 Instructions

**Vector Search:**
- Enter a query in natural language
- The system finds semantically similar chunks
- Results are sorted by relevance

**Parameters:**
- **Top K:** Number of results to return
- **Probes:** Higher value = more precision but slower
- **Max Distance:** Similarity threshold (lower = stricter)

**Use Cases:**
- Explore document content
- Verify what information is available
- Debugging the retrieval system
        """)
