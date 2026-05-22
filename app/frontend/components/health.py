import asyncio
import gradio as gr

from app.frontend.api_client import AtlasAPIClient


def create_health_tab(client: AtlasAPIClient):
    async def check_health():
        try:
            result = await client.health_check()
            status = f"✅ The service is functioning properly"
            details = f"""
**Status:** {result['status']}
**Service Name:** {result['service']}
**Version:** {result['version']}
**Check Time:** {result['timestamp']}
            """
            return status, details

        except Exception as e:
            status = "❌ Service is down or unreachable"
            details = f"**Error:** {str(e)}"
            return status, details

    def sync_check_health():
        return asyncio.run(check_health())

    with gr.Tab("🏥 Health Check"):
        gr.Markdown("## System status")

        check_btn = gr.Button("🔄 Check Status", variant="primary")

        with gr.Row():
            with gr.Column():
                health_status = gr.Textbox(label="Status", interactive=False, lines=1)
            with gr.Column():
                health_details = gr.Markdown()

        check_btn.click(fn=sync_check_health, outputs=[health_status, health_details])
