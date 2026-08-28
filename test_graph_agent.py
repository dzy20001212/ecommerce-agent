from graph_agent import graph_agent


test_cases = [
    "订单10001发货了吗？",
    "AirSound Pro支持主动降噪吗？",
    "订单10001的快递到哪里了？",
    "商品签收后还能退货吗？",
    "我要人工客服",
    "你好",
    "订单10001里的商品支持主动降噪吗？",
]


for index, question in enumerate(
    test_cases,
    start=1
):

    config = {
        "configurable": {
            "thread_id": f"test_{index}"
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

    print("=" * 60)

    print(
        "Question:",
        question
    )

    print(
        "Answer:",
        result["messages"][-1].content
    )

    print(
        "LLM Calls:",
        result["llm_calls"]
    )