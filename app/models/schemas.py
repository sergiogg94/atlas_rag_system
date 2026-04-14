from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for a question to query the RAG service.

    Attributes:
        question (str): The user's question to process.
    """

    question: str = Field(
        ...,
        description="User question to be processed",
        example="What is the capital of France?",
        min_length=1,
        max_length=500,
    )


class QueryResponse(BaseModel):
    """Response model returned by the RAG service.

    Attributes:
        response (str): The generated answer text.
        sources (list[str]): A list of sources used to generate the answer.
    """

    response: str = Field(
        ...,
        description="Answer generated",
        example="The capital of France is Paris.",
    )
    sources: list[str] = Field(
        [],
        description="List of sources used to generate the answer",
    )
