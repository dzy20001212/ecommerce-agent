import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

from tools import (
    search_product,
    query_order,
    search_policy,
    query_logistics,
    transfer_to_human,
)


load_dotenv()


model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
)


tools = [
    search_product,
    query_order,
    search_policy,
    query_logistics,
    transfer_to_human,
]


model_with_tools = model.bind_tools(tools)




test_cases = [

    ("订单10001发货了吗？", "query_order"),

    ("我买的10002是什么商品？", "query_order"),

    ("AirSound Pro多少钱？", "search_product"),

    ("SmartWatch X1防水吗？", "search_product"),

    ("商品没发货可以退款吗？", "search_policy"),

    ("商品签收后几天可以退货？", "search_policy"),

    ("订单10001的快递到哪里了？", "query_logistics"),

    ("10001现在运输到哪一步了？", "query_logistics"),

    ("我要找人工客服", "transfer_to_human"),

    ("我要人工处理这个问题", "transfer_to_human"),

    ("你好", None),

    ("谢谢你", None),

]



correct = 0


for question, expected_tool in test_cases:

    response = model_with_tools.invoke(
        [
            (
                "system",
                """
                你是一名电商客服。
                请根据用户问题选择最合适的工具。
                如果不需要工具，可以直接回答。
                """
            ),
            (
                "human",
                question
            )
        ]
    )


    if response.tool_calls:
        actual_tool = response.tool_calls[0]["name"]
    else:
        actual_tool = None


    is_correct = actual_tool == expected_tool


    if is_correct:
        correct += 1


    print("=" * 50)

    print("Question:", question)

    print("Expected:", expected_tool)

    print("Actual:", actual_tool)

    print(
        "Result:",
        "PASS" if is_correct else "FAIL"
    )

accuracy = correct / len(test_cases)


print("\n===== Final Result =====")

print(
    f"Tool Selection Accuracy: "
    f"{accuracy:.2%}"
)