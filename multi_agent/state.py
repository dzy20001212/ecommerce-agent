# from typing import TypedDict, Any


# class MultiAgentState(
#     TypedDict,
#     total=False
# ):

#     # =================================
#     # 用户请求
#     # =================================

#     user_query: str


#     # =================================
#     # Supervisor Routing
#     # =================================

#     route: str

#     current_agent: str


#     # =================================
#     # 业务上下文
#     # =================================

#     order_id: str

#     product_name: str


#     # =================================
#     # Agent / Tool结果
#     # =================================

#     tool_result: Any

#     agent_result: str

#     final_answer: str


#     # =================================
#     # 对话信息
#     # 后面可以和原LangGraph State继续整合
#     # =================================

#     messages: list


#     # =================================
#     # Week 7 Observability预留
#     # Day 4会正式使用
#     # =================================

#     request_id: str

#     routing_count: int




from typing import TypedDict, Any


class MultiAgentState(
    TypedDict,
    total=False
):
    # 用户原始问题
    user_query: str

    # Supervisor首次路由
    route: str
    initial_route: str

    # 当前Agent
    current_agent: str

    # 业务信息
    order_id: str
    product_name: str

    # Worker执行结果
    tool_result: Any
    agent_result: str

    # Order Agent查询出来的信息
    order_context: str

    # Agent交接
    handoff_to: str
    handoff_reason: str
    handoff_count: int

    # 已经执行过哪些Agent
    visited_agents: list[str]

    # 最终回答
    final_answer: str

    # 后续继续使用
    messages: list

    # Observability预留
    request_id: str

    node_latencies: dict[str, float]

    tool_calls: list[str]

    llm_calls: int

    errors: list[str]

    total_latency_ms: float