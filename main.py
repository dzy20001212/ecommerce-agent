from fastapi import FastAPI

from app.api.routes import (
    router,
)


app = FastAPI(
    title="E-commerce Multi-Agent API",
    description=(
        "基于LangChain、LangGraph构建的"
        "电商Multi-Agent客服服务"
    ),
    version="1.0.0",
)


app.include_router(
    router,
)