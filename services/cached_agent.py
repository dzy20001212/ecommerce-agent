import time
import uuid

from graph_agent import graph_agent

from cache.redis_cache import (
    build_cache_key,
    get_json,
    set_json,
)


SAFE_CACHE_TOOLS = {
    "search_product",
    "search_policy",
}


def extract_used_tools(messages):
    """
    从 Agent 执行轨迹中提取实际调用的 Tool。
    """

    used_tools = []

    for message in messages:

        tool_calls = getattr(
            message,
            "tool_calls",
            None
        )

        if not tool_calls:
            continue

        for tool_call in tool_calls:

            used_tools.append(
                tool_call["name"]
            )

    return used_tools


def can_cache_response(
    used_tools
) -> bool:
    """
    只有真正调用过 Tool，
    且全部属于静态安全 Tool，
    才允许缓存最终回答。
    """

    if not used_tools:
        return False

    return set(
        used_tools
    ).issubset(
        SAFE_CACHE_TOOLS
    )


def ask_stateless_with_cache(
    question: str
):
    """
    单轮、无上下文 FAQ 查询。

    注意：
    这个函数暂时不用于 Memory 多轮对话。
    """

    start_time = time.perf_counter()

    cache_key = build_cache_key(
        namespace="response",
        text=question,
    )

    cached = get_json(cache_key)

    if cached is not None:

        elapsed_ms = (
            time.perf_counter()
            - start_time
        ) * 1000

        return {
            "answer": cached["answer"],
            "cache_hit": True,
            "cache_key": cache_key,
            "elapsed_ms": elapsed_ms,
            "llm_calls": 0,
            "tool_calls": 0,
            "used_tools": cached.get(
                "used_tools",
                []
            ),
        }


    # Cache Miss：正常运行 Agent

    thread_id = (
        "stateless_"
        + str(uuid.uuid4())
    )

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }


    result = graph_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ],
            "llm_calls": 0,
        },
        config,
    )


    answer = (
        result["messages"][-1].content
    )


    used_tools = extract_used_tools(
        result["messages"]
    )


    if can_cache_response(
        used_tools
    ):

        set_json(
            cache_key,
            {
                "answer": answer,
                "used_tools": used_tools,
            },
        )


    elapsed_ms = (
        time.perf_counter()
        - start_time
    ) * 1000


    return {
        "answer": answer,
        "cache_hit": False,
        "cache_key": cache_key,
        "elapsed_ms": elapsed_ms,
        "llm_calls": result.get(
            "llm_calls",
            0
        ),
        "tool_calls": len(
            used_tools
        ),
        "used_tools": used_tools,
    }