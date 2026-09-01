from langchain.agents import create_agent

from agents.model import create_model

from tools import (
    search_product,
)


model = create_model()


PRODUCT_SYSTEM_PROMPT = """
你是电商客服系统中的商品专家 Product Agent。

你的职责仅限于处理商品相关问题，例如：
- 商品价格
- 商品属性
- 商品功能
- 商品基本信息

可以使用的Tool：
- search_product

如果需要查询商品真实信息，应优先调用Tool，
不要凭空编造商品数据。

不要处理订单、物流、退款、退货或人工客服问题。
"""


product_agent = create_agent(
    model=model,
    tools=[
        search_product,
    ],
    system_prompt=(
        PRODUCT_SYSTEM_PROMPT
    ),
)


def run_product_agent(
    user_query: str
) -> str:

    result = product_agent.invoke(
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