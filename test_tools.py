from tools import (
    search_product,
    query_order,
    query_logistics,
    search_policy,
    transfer_to_human,
)


print(
    search_product.invoke(
        {"product_name": "AirSound Pro"}
    )
)


print(
    query_order.invoke(
        {"order_id": "10001"}
    )
)


print(
    query_logistics.invoke(
        {"order_id": "10001"}
    )
)


print(
    search_policy.invoke(
        {"topic": "退款"}
    )
)


print(
    transfer_to_human.invoke(
        {"reason": "用户要求人工处理投诉"}
    )
)