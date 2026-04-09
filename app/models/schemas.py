from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        description="User question to be processed",
        example="What is the capital of France?",
        min_length=1,
        max_length=500,
    )


class QueryResponse(BaseModel):
    response: str = Field(
        ...,
        description="Answer generated",
        example="The capital of France is Paris.",
    )
    sources: list[str] = Field(
        [],
        description="List of sources used to generate the answer",
    )
