import asyncio

import gradio as gr

from app.frontend.api_client import AtlasAPIClient


def create_collections_tab(client: AtlasAPIClient):
    async def load_collections():
        """Loads all collections and returns dropdown options"""
        collections = await client.list_collections()

        if not collections:
            return [], "No collections", ""

        choices = [
            (f"{c['name']} ({c['provider']} / {c['model']})", c["id"])
            for c in collections
        ]
        table = "| ID | Name | Provider | Model | Dimension |\n|---|---|---|---|---|\n"
        for c in collections:
            table += f"| {c['id']} | {c['name']} | {c['provider']} | {c['model']} | {c['dimension']} |\n"
        return choices, "✅ Collections loaded", table

    async def create_collection_handler(name, provider, model, dimension, description):
        if not name or not provider or not model or not dimension:
            return "⚠️ Name, provider, model and dimension are required", ""
        try:
            result = await client.create_collection(
                name=name,
                provider=provider,
                model=model,
                dimension=int(dimension),
                description=description or "",
            )
            return f"✅ Collection '{result['name']}' created (id={result['id']})", ""
        except Exception as e:  # noqa: BLE001
            return f"❌ Error: {e}", ""

    async def load_catalog():
        """Loads providers catalog for the dropdown."""
        catalog = await client.get_provider_catalog()
        return catalog

    def sync_load():
        _, status, table = asyncio.run(load_collections())
        return status, table

    def sync_create(name, provider, model, dimension, description):
        status, _ = asyncio.run(
            create_collection_handler(name, provider, model, dimension, description)
        )
        return status

    ## Start Gradio UI
    with gr.Tab("🗂️ Collections"):
        gr.Markdown("## Vector collections managment")

        with gr.Tabs():
            # Tab: list
            with gr.Tab("📋 View collections"):
                with gr.Row():
                    refresh_btn = gr.Button("🔄 Load collections", variant="secondary")
                list_status = gr.Textbox(label="Status", interactive=False)
                collections_table = gr.Markdown()

                refresh_btn.click(
                    fn=sync_load,
                    outputs=[list_status, collections_table],
                )

            # Tab: create
            with gr.Tab("➕ New collection"):
                with gr.Row():
                    with gr.Column():
                        new_name = gr.Textbox(
                            label="Name *",
                            placeholder="legal-documents",
                        )
                        new_description = gr.Textbox(
                            label="Description (optional)",
                            placeholder="What is this collection used for?",
                        )
                        new_provider = gr.Dropdown(
                            label="Provider *",
                            choices=["voyage", "local"],
                            value="local",
                        )
                        new_model = gr.Dropdown(
                            label="Model *",
                            choices=[
                                "sentence-transformers/all-MiniLM-L6-v2",
                                "sentence-transformers/all-mpnet-base-v2",
                                "BAAI/bge-small-en-v1.5",
                                "voyage-3-lite",
                                "voyage-3",
                                "voyage-4",
                            ],
                            value="sentence-transformers/all-MiniLM-L6-v2",
                        )
                        new_dimension = gr.Number(
                            label="Dimension *",
                            value=384,
                            minimum=64,
                            maximum=4096,
                            info="Check the dimensions of the model you selected.",
                        )

                        create_btn = gr.Button(
                            "✨ Create collection", variant="primary"
                        )

                    with gr.Column():
                        create_status = gr.Textbox(label="Status", interactive=False)
                        gr.Markdown("""
### 📚 Quick reference for dimensions

| Model | Dimension |
|--------|-----------|
| all-MiniLM-L6-v2 | 384 |
| all-mpnet-base-v2 | 768 |
| bge-small-en-v1.5 | 384 |
| voyage-3-lite | 512 |
| voyage-3 | 1024 |
| voyage-4 | 1024-2048 |
                        """)

                create_btn.click(
                    fn=sync_create,
                    inputs=[
                        new_name,
                        new_provider,
                        new_model,
                        new_dimension,
                        new_description,
                    ],
                    outputs=[create_status],
                )
