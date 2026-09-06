import re


AFTER_SALES_KEYWORDS = [
    "退货",
    "退款",
    "换货",
    "售后",
    "可以退",
    "能退",
    "能不能退",
]


def needs_service_after_order(
    user_query: str
) -> bool:

    if not user_query:
        return False

    return any(
        keyword in user_query
        for keyword
        in AFTER_SALES_KEYWORDS
    )


def extract_order_id(
    user_query: str
) -> str:

    match = re.search(
        r"\b\d{5,}\b",
        user_query
    )

    if match:
        return match.group(0)

    return ""


def order_lookup_failed(
    order_result: str
) -> bool:

    failure_keywords = [
        "未找到",
        "不存在",
        "没有查询到",
        "未查询到",
    ]

    return any(
        keyword in str(order_result)
        for keyword
        in failure_keywords
    )