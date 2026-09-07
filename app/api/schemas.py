from pydantic import BaseModel, Field


class ChatRequest(BaseModel):

    message: str = Field(
        ...,
        min_length=1,
        description="用户发送给电商客服Agent的问题",
    )

class ChatResponse(BaseModel):

    request_id: str

    answer: str

    route: str | None = None

    agents: list[str]

    tools: list[str]

    llm_calls: int

    handoff_count: int

    latency_ms: float

class HealthResponse(BaseModel):

    status: str

    service: str