from typing import TypedDict, Any


class MultiAgentState(
    TypedDict,
    total=False
):

    # =================================
    # 用户请求
    # =================================

    user_query: str


    # =================================
    # Supervisor Routing
    # =================================

    route: str

    current_agent: str


    # =================================
    # 业务上下文
    # =================================

    order_id: str

    product_name: str


    # =================================
    # Agent / Tool结果
    # =================================

    tool_result: Any

    agent_result: str

    final_answer: str


    # =================================
    # 对话信息
    # 后面可以和原LangGraph State继续整合
    # =================================

    messages: list


    # =================================
    # Week 7 Observability预留
    # Day 4会正式使用
    # =================================

    request_id: str

    routing_count: int