from typing import Literal

from pydantic import BaseModel

from agents.model import create_model


model = create_model()


class RouteDecision(
    BaseModel
):

    route: Literal[
        "product",
        "order",
        "service",
    ]

SUPERVISOR_PROMPT = """
你是电商客服 Multi-Agent 系统的 Supervisor。

你的任务不是直接回答用户问题，
而是判断用户问题应该交给哪个专业Agent。

可选路由只有：

product:
商品价格、商品属性、商品功能、商品信息。

order:
订单状态、订单商品、发货状态、物流、快递进度。

service:
退款、退货、换货、售后政策、人工客服。

必须只从 product、order、service 中选择一个。
"""

structured_model = (
    model.with_structured_output(
        RouteDecision
    )
)

def decide_route(
    user_query: str
) -> str:

    prompt = (
        SUPERVISOR_PROMPT
        + "\n\n用户问题："
        + user_query
    )


    decision = (
        structured_model.invoke(
            prompt
        )
    )


    return decision.route

