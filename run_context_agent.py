from graph_agent_context import (
    graph_agent
)


THREAD_ID = (
    "context_customer_001"
)


config = {
    "configurable": {
        "thread_id": THREAD_ID
    }
}


while True:

    question = input(
        "\n用户："
    )


    if question.lower() in [
        "quit",
        "exit",
    ]:
        break


    result = graph_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ],

            "llm_calls": 0,

            "summary_calls": 0,
        },
        config,
    )


    print(
        "\nAgent：",
        result["messages"][-1].content
    )


    print(
        "\n===== Context Metrics ====="
    )

    print(
        "Full State Tokens:",
        result.get(
            "full_state_tokens",
            0
        )
    )

    print(
        "Model Context Tokens:",
        result.get(
            "model_context_tokens",
            0
        )
    )

    print(
        "Summary Calls:",
        result.get(
            "summary_calls",
            0
        )
    )

    print(
        "Summarized Messages:",
        result.get(
            "summarized_count",
            0
        )
    )

    print(
        "Current Summary:",
        result.get(
            "summary",
            "暂无摘要"
        )
    )