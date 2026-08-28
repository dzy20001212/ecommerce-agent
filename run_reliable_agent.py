from graph_agent_reliable import (
    graph_agent
)


THREAD_ID = (
    "reliable_customer_001"
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

            "tool_retries": 0,

            "tool_failures": 0,

            "fallback_count": 0,
        },
        config,
    )


    print(
        "\nAgent："
    )

    print(
        result["messages"][-1].content
    )


    print(
        "\n===== Reliability Metrics ====="
    )

    print(
        "Tool Retries:",
        result.get(
            "tool_retries",
            0
        )
    )

    print(
        "Tool Failures:",
        result.get(
            "tool_failures",
            0
        )
    )

    print(
        "Fallback Count:",
        result.get(
            "fallback_count",
            0
        )
    )

    print(
        "Last Error:",
        result.get(
            "last_error",
            ""
        )
    )