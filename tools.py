import json

from langchain.tools import tool
from pydantic import BaseModel, Field

from data_loader import (
    PRODUCTS,
    ORDERS,
    LOGISTICS,
    POLICIES,
)



class ProductQueryInput(BaseModel):
    product_name: str = Field(
        description="需要查询的完整商品名称，例如 AirSound Pro"
    )


class OrderQueryInput(BaseModel):
    order_id: str = Field(
        description="用户订单编号，例如10001，不包含其他文本"
    )


class LogisticsQueryInput(BaseModel):
    order_id: str = Field(
        description="需要查询物流运输状态的订单编号，例如10001"
    )


class PolicyQueryInput(BaseModel):
    topic: str = Field(
        description="售后政策主题，例如退款、退货或换货"
    )


class HumanServiceInput(BaseModel):
    reason: str = Field(
        description="用户需要人工客服的原因"
    )



@tool(args_schema=ProductQueryInput)
def search_product(product_name: str) -> str:
    """
    根据商品名称查询商品详细信息。

    适用于：
    - 商品价格
    - 商品颜色
    - 商品功能
    - 商品参数
    - 商品是否支持某项功能

    不用于订单、物流和售后政策查询。
    """

    product = PRODUCTS.get(product_name)

    if not product:
        return "没有找到该商品"

    return json.dumps(
        product,
        ensure_ascii=False
    )




@tool(args_schema=OrderQueryInput)
def query_order(order_id: str) -> str:
    """
    根据订单编号查询订单基本信息。

    适用于：
    - 查询订单状态
    - 判断订单是否发货
    - 查询订单购买了什么商品

    不用于查询具体物流运输节点。
    """

    order = ORDERS.get(order_id)

    if not order:
        return "没有找到该订单"

    return json.dumps(
        order,
        ensure_ascii=False
    )




@tool(args_schema=PolicyQueryInput)
def search_policy(topic: str) -> str:
    """
    查询商城售后政策。

    适用于：
    - 退款
    - 退货
    - 换货
    - 售后规则

    不用于查询具体订单或物流状态。
    """

    policy = POLICIES.get(topic)

    if not policy:
        return "暂未找到相关售后政策"

    return policy





@tool(args_schema=LogisticsQueryInput)
def query_logistics(order_id: str) -> str:
    """
    根据订单编号查询物流运输信息。

    适用于：
    - 快递到哪里了
    - 当前物流运输状态
    - 快递公司
    - 快递单号
    - 最新物流节点

    如果只是询问订单是否发货，
    优先使用 query_order。
    """

    logistics = LOGISTICS.get(order_id)

    if not logistics:
        return "没有找到该订单的物流信息"

    return json.dumps(
        logistics,
        ensure_ascii=False
    )


@tool(args_schema=HumanServiceInput)
def transfer_to_human(reason: str) -> str:
    """
    将问题转交人工客服。

    仅适用于：
    - 用户明确要求人工客服
    - 用户明确要求人工投诉处理
    - 用户要求人工介入

    普通商品、订单、物流和售后问题
    不应该直接调用本工具。
    """

    return (
        f"已创建人工客服请求。"
        f"转人工原因：{reason}。"
        f"请等待人工客服接入。"
    )