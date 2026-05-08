from openai import AsyncOpenAI
from app.core.config import settings


class LLMService:
    def __init__(self, system_prompt: str = None):
        self.client = AsyncOpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=settings.hf_token,
        )
        self.model = "katanemo/Arch-Router-1.5B:hf-inference"
        self.system_prompt = system_prompt or self._default_system_prompt()

    def _default_system_prompt(self) -> str:
        """Default system prompt for the LLM to guide its responses."""
        system_prompt = """You are a helpful assistant that helps users to answer question about the content of a document.
You will be given a question and a document, and you need to provide an answer based ONLY on the content of the document.

Important rules:
1. You should only use the information provided in the document to answer the question
2. If the document does not contain enough information to answer the question, you should say "I don't found information in the disponible documents"
3. Always answer in a concise manner
4. If the context is ambiguous, you should mention different possibilities
5. You should not make up any information that is not present in the document
"""
        return system_prompt

    def set_system_prompt(self, prompt: str):
        """To change the system prompt at runtime."""
        self.system_prompt = prompt

    def _build_messages(self, query: str, context: str) -> str:
        """Build the message for openai API based on the system prompt, query and context."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"# Context: {context}\n\n# Question: {query}"},
        ]
        return messages

    async def get_answer(
        self, query: str, context: str, max_tokens: int = 512, temperature: float = 0.7
    ) -> str:
        """Get an answer from the LLM based on the query and context."""
        messages = self._build_messages(query, context)

        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return completion.choices[0].message.content
