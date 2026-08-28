from graph_agent import graph_agent


THREAD_ID = "graph_customer_001"


config = {
    "configurable": {
        "thread_id": THREAD_ID
    }
}


while True:

    question = input("\n用户：")

    if question.lower() in [
        "quit",
        "exit"
    ]:
        print("会话结束。")
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
        },
        config,
    )


    print("\nAgent：")
    print(
        result["messages"][-1].content
    )

    print(
        "\n本次状态中的 LLM 调用次数：",
        result["llm_calls"]
    )