import asyncio

import gradio as gr

from app.frontend.api_client import AtlasAPIClient


def create_health_tab(client: AtlasAPIClient):
    async def check_health():
        try:
            result = await client.health_check()
            status = "✅ The service is functioning properly"
            details = f"""
**Status:** {result["status"]}
**Service Name:** {result["service"]}
**Version:** {result["version"]}
**Check Time:** {result["timestamp"]}
            """
            return status, details

        except Exception as e:  # noqa: BLE001
            status = "❌ Service is down or unreachable"
            details = f"**Error:** {e!s}"
            return status, details

    def sync_check_health():
        return asyncio.run(check_health())

    with gr.Tab("🏥 Health Check"):
        gr.Markdown("## System status")

        check_btn = gr.Button("🔄 Check Status", variant="primary", scale=0)

        with gr.Row():
            with gr.Column():
                health_status = gr.Textbox(label="Status", interactive=False, lines=1)
            with gr.Column():
                health_details = gr.Markdown()

        check_btn.click(fn=sync_check_health, outputs=[health_status, health_details])
