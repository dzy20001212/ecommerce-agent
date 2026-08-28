from services.secure_agent import (
    ask_secure_agent,
)


questions = [

    "我的订单号是10001",

    "它发货了吗？",

    "这个订单购买了什么商品？",

    "这个商品支持主动降噪吗？",

    "商品签收以后可以退货吗？",

    "那这个订单物流现在到哪里了？",

    "再告诉我刚才说的订单号是多少？",

    "它现在是什么物流状态？",
]


THREAD_ID = (
    "context_eval_001"
)


for index, question in enumerate(
    questions,
    start=1,
):

    result = ask_secure_agent(
        question,
        THREAD_ID,
    )


    print(
        "\n"
        "================================"
    )

    print(
        f"Turn {index}"
    )

    print(
        "================================"
    )


    print(
        "Question:",
        question
    )


    print(
        "Answer:",
        result["answer"]
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
