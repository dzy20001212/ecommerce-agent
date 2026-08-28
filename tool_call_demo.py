# Agent Tool Loop 的简化底层实现代码
import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

from tools import (
    search_product,
    query_order,
    search_policy,
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
]


tool_map = {
    tool.name: tool
    for tool in tools
}


model_with_tools = model.bind_tools(tools)


messages = [
    (
        "system",
        """
        你是一名电商客服助手。
        根据用户问题决定是否调用工具。
        不允许编造订单、商品或售后信息。
        """
    ),
    (
        "human",
        "订单10001发货了吗？"
    )
]


# 第一次调用模型
ai_message = model_with_tools.invoke(messages)

messages.append(ai_message)


print("第一次模型输出：")
print(ai_message.tool_calls)


# 真正执行工具
for tool_call in ai_message.tool_calls:

    selected_tool = tool_map[tool_call["name"]]

    tool_message = selected_tool.invoke(tool_call)

    messages.append(tool_message)

    print("\nTool执行结果：")
    print(tool_message)


# 第二次调用模型
final_response = model_with_tools.invoke(messages)


print("\n最终回答：")
print(final_response.content)