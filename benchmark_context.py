from langchain.messages import (
    HumanMessage,
    AIMessage,
)

from utils.context_manager import (
    count_message_tokens,
    trim_context,
)


messages = []


for i in range(20):

    messages.append(
        HumanMessage(
            content=(
                f"这是用户第{i + 1}轮问题，"
                "我正在咨询订单、商品、物流和售后信息。"
            )
        )
    )

    messages.append(
        AIMessage(
            content=(
                f"这是客服第{i + 1}轮回答，"
                "已经记录并处理当前问题。"
            )
        )
    )


before_tokens = (
    count_message_tokens(messages)
)


trimmed_messages = trim_context(
    messages,
    max_tokens=300,
)


after_tokens = (
    count_message_tokens(
        trimmed_messages
    )
)


print(
    "原始消息数量：",
    len(messages)
)

print(
    "原始 Token：",
    before_tokens
)

print(
    "裁剪后消息数量：",
    len(trimmed_messages)
)

print(
    "裁剪后 Token：",
    after_tokens
)

print(
    "\n===== Context Optimization ====="
)

print(
    "Full Tokens:",
    before_tokens
)

print(
    "Trimmed Tokens:",
    after_tokens
)

reduction_rate = (
    1
    - after_tokens
    / before_tokens
)

print(
    "Token Reduction:",
    f"{reduction_rate:.2%}"
)