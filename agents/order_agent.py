from langchain.agents import create_agent

from agents.model import create_model

from tools import (
    query_order,
    query_logistics,
)

from observability.agent_metrics import (
    summarize_agent_messages,
)

model = create_model()


ORDER_SYSTEM_PROMPT = """
你是电商客服系统中的订单专家 Order Agent。

你的职责包括：
- 查询订单信息
- 查询订单状态
- 查询订单商品
- 查询物流状态
- 查询物流节点

可以使用的Tool：
- query_order
- query_logistics

订单问题优先使用 query_order。
物流、快递、运输进度问题优先使用 query_logistics。

不要凭空编造订单或物流数据。

不要处理商品价格、退款政策或人工客服问题。
"""


order_agent = create_agent(
    model=model,
    tools=[
        query_order,
        query_logistics,
    ],
    system_prompt=(
        ORDER_SYSTEM_PROMPT
    ),
)


def run_order_agent_detailed(
    user_query: str
):

    result = order_agent.invoke(
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


    return summarize_agent_messages(
        result["messages"]
    )


def run_order_agent(
    user_query: str
) -> str:

    detail = (
        run_order_agent_detailed(
            user_query
        )
    )

    return detail["answer"]