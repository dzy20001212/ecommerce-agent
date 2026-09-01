from langchain.agents import create_agent

from agents.model import create_model

from tools import (
    search_policy,
    transfer_to_human,
)


model = create_model()


SERVICE_SYSTEM_PROMPT = """
你是电商客服系统中的售后服务专家 Service Agent。

你的职责包括：
- 退款政策
- 退货政策
- 换货政策
- 售后问题
- 人工客服

可以使用的Tool：
- search_policy
- transfer_to_human

退款、退货、换货等政策问题优先调用 search_policy。

只有用户明确要求人工客服时，
才允许调用 transfer_to_human。

不要处理商品价格、订单状态和物流查询。
"""


service_agent = create_agent(
    model=model,
    tools=[
        search_policy,
        transfer_to_human,
    ],
    system_prompt=(
        SERVICE_SYSTEM_PROMPT
    ),
)


def run_service_agent(
    user_query: str
) -> str:

    result = service_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content":
                        user_query,
                }
            ]
        }
    )

    return (
        result["messages"][-1]
        .content
    )