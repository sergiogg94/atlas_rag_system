import gradio as gr


def greet():
    return "Hello from Atlas RAG System"


def main():
    with gr.Blocks() as app:
        gr.Markdown("## Atlas RAG System")
        greet_button = gr.Button("Greet")
        output = gr.Textbox(label="Output")

        greet_button.click(fn=greet, outputs=output)

    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
    )


if __name__ == "__main__":
    main()
