# =====================================
# Week 7 Day 1
# Multi-Agent Routing Definition
# =====================================


PRODUCT_ROUTE = "product"

ORDER_ROUTE = "order"

SERVICE_ROUTE = "service"


VALID_ROUTES = {
    PRODUCT_ROUTE,
    ORDER_ROUTE,
    SERVICE_ROUTE,
}


# =====================================
# 每个Agent允许使用的Tool
# =====================================

AGENT_TOOL_MAPPING = {

    PRODUCT_ROUTE: [
        "search_product",
    ],

    ORDER_ROUTE: [
        "query_order",
        "query_logistics",
    ],

    SERVICE_ROUTE: [
        "search_policy",
        "transfer_to_human",
    ],
}


# =====================================
# Agent职责描述
#
# Day 2 Supervisor会使用类似信息
# 做真正的LLM Routing
# =====================================

AGENT_DESCRIPTIONS = {

    PRODUCT_ROUTE:
        (
            "负责商品相关问题，"
            "包括商品价格、属性、功能和商品信息查询。"
        ),

    ORDER_ROUTE:
        (
            "负责订单和物流相关问题，"
            "包括订单状态、购买商品、发货状态和物流进度。"
        ),

    SERVICE_ROUTE:
        (
            "负责售后和人工服务相关问题，"
            "包括退款、退货、换货政策以及人工客服。"
        ),
}