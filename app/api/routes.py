from fastapi import (
    APIRouter,
    HTTPException,
)

from app.api.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
)

from app.services.chat_service import (
    chat,
)


router = APIRouter()

@router.get(
    "/health",
    response_model=HealthResponse,
)
def health_check():

    return {
        "status": "ok",
        "service": "ecommerce-agent",
    }

@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat_endpoint(
    request: ChatRequest,
):

    try:

        result = chat(
            request.message
        )

        return ChatResponse(
            request_id=
                result["request_id"],

            answer=
                result["answer"],

            route=
                result["route"],

            agents=
                result["agents"],

            tools=
                result["tools"],

            llm_calls=
                result["llm_calls"],

            handoff_count=
                result[
                    "handoff_count"
                ],

            latency_ms=
                result[
                    "latency_ms"
                ],
        )


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Agent执行失败：{str(e)}"
            ),
        )

    