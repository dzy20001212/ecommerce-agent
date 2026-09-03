from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from multi_agent.state import (
    MultiAgentState,
)

from multi_agent.handoff import (
    needs_service_after_order,
    extract_order_id,
    order_lookup_failed,
)

from agents.supervisor import (
    decide_route,
)

from time import perf_counter

from observability.tracer import (
    log_event,
)

from agents.product_agent import (
    run_product_agent_detailed,
)

from agents.order_agent import (
    run_order_agent_detailed,
)

from agents.service_agent import (
    run_service_agent_detailed,
)

def supervisor_node(
    state: MultiAgentState
):

    request_id = (
        state["request_id"]
    )

    start = perf_counter()


    log_event(
        request_id,
        "node_start",
        node="supervisor",
    )


    try:

        route = decide_route(
            state["user_query"]
        )


        latency_ms = (
            perf_counter()
            - start
        ) * 1000


        latencies = dict(
            state.get(
                "node_latencies",
                {}
            )
        )

        latencies[
            "supervisor"
        ] = latency_ms


        log_event(
            request_id,
            "supervisor_end",
            route=route,
            latency_ms=latency_ms,
        )


        return {
            "route":
                route,

            "initial_route":
                route,

            "handoff_count":
                0,

            "visited_agents":
                [],

            "llm_calls":
                state.get(
                    "llm_calls",
                    0
                ) + 1,

            "node_latencies":
                latencies,
        }


    except Exception as e:

        log_event(
            request_id,
            "error",
            node="supervisor",
            error_type=
                type(e).__name__,
            message=str(e),
        )

        raise

def product_node(
    state: MultiAgentState
):

    request_id = (
        state["request_id"]
    )

    start = perf_counter()


    log_event(
        request_id,
        "node_start",
        node="product",
    )


    try:

        detail = (
            run_product_agent_detailed(
                state["user_query"]
            )
        )


        latency_ms = (
            perf_counter()
            - start
        ) * 1000


        tools = (
            state.get(
                "tool_calls",
                []
            )
            + detail[
                "tool_names"
            ]
        )


        for tool_name in (
            detail["tool_names"]
        ):

            log_event(
                request_id,
                "tool_used",
                agent="product",
                tool=tool_name,
            )


        latencies = dict(
            state.get(
                "node_latencies",
                {}
            )
        )

        latencies[
            "product"
        ] = latency_ms


        visited = (
            state.get(
                "visited_agents",
                []
            )
            + ["product"]
        )


        log_event(
            request_id,
            "agent_end",
            agent="product",
            latency_ms=latency_ms,
            llm_calls=
                detail["llm_calls"],
        )


        return {
            "current_agent":
                "product",

            "agent_result":
                detail["answer"],

            "final_answer":
                detail["answer"],

            "visited_agents":
                visited,

            "tool_calls":
                tools,

            "llm_calls":
                state.get(
                    "llm_calls",
                    0
                )
                + detail[
                    "llm_calls"
                ],

            "node_latencies":
                latencies,
        }


    except Exception as e:

        log_event(
            request_id,
            "error",
            node="product",
            error_type=
                type(e).__name__,
            message=str(e),
        )

        raise

def order_node(
    state: MultiAgentState
):

    request_id = state["request_id"]

    start = perf_counter()

    print(
        "\n[Order Agent] Start"
    )

    log_event(
        request_id,
        "node_start",
        node="order",
    )


    try:

        user_query = state["user_query"]


        need_service = (
            needs_service_after_order(
                user_query
            )
        )


        # 如果后面还需要售后 Agent，
        # Order Agent 只负责先查询订单事实
        if need_service:

            order_task = f"""
请只查询下面问题涉及的订单信息，
不要回答退款、退货、换货政策。

用户原始问题：
{user_query}
"""

        else:

            order_task = user_query


        # =================================
        # 执行 Order Agent
        # =================================

        detail = (
            run_order_agent_detailed(
                order_task
            )
        )

        answer = detail["answer"]


        # =================================
        # 统计 Tool
        # =================================

        tools = (
            state.get(
                "tool_calls",
                []
            )
            + detail["tool_names"]
        )


        for tool_name in (
            detail["tool_names"]
        ):

            log_event(
                request_id,
                "tool_used",
                agent="order",
                tool=tool_name,
            )


        # =================================
        # 统计耗时
        # =================================

        latency_ms = (
            perf_counter()
            - start
        ) * 1000


        latencies = dict(
            state.get(
                "node_latencies",
                {}
            )
        )

        latencies[
            "order"
        ] = latency_ms


        # =================================
        # Visited Agents
        # =================================

        visited = (
            state.get(
                "visited_agents",
                []
            )
            + ["order"]
        )


        order_id = extract_order_id(
            user_query
        )


        # =================================
        # 判断订单是否查询失败
        # =================================

        failed = order_lookup_failed(
            answer
        )


        # =================================
        # 判断是否 Handoff
        # =================================

        if (
            need_service
            and not failed
        ):

            handoff_to = "service"

            handoff_reason = (
                "订单事实已经查询完成，"
                "用户还有售后需求，"
                "交给Service Agent。"
            )

            handoff_count = (
                state.get(
                    "handoff_count",
                    0
                )
                + 1
            )


            log_event(
                request_id,
                "handoff",
                from_agent="order",
                to_agent="service",
                reason=handoff_reason,
            )

        else:

            handoff_to = "end"

            if failed:

                handoff_reason = (
                    "订单查询失败，"
                    "停止后续Agent调用。"
                )

            else:

                handoff_reason = (
                    "订单任务已经完成。"
                )


            handoff_count = (
                state.get(
                    "handoff_count",
                    0
                )
            )


        print(
            f"[Order Agent] "
            f"handoff_to="
            f"{handoff_to}"
        )


        # =================================
        # Agent结束日志
        # =================================

        log_event(
            request_id,
            "agent_end",
            agent="order",
            latency_ms=latency_ms,
            llm_calls=
                detail["llm_calls"],
        )


        # =================================
        # 写回 LangGraph State
        # =================================

        return {

            "current_agent":
                "order",

            "order_id":
                order_id,

            "order_context":
                answer,

            "agent_result":
                answer,

            "final_answer":
                answer,

            "handoff_to":
                handoff_to,

            "handoff_reason":
                handoff_reason,

            "handoff_count":
                handoff_count,

            "visited_agents":
                visited,

            # Day 4新增
            "tool_calls":
                tools,

            "llm_calls":
                state.get(
                    "llm_calls",
                    0
                )
                + detail[
                    "llm_calls"
                ],

            "node_latencies":
                latencies,
        }


    except Exception as e:

        log_event(
            request_id,
            "error",
            node="order",
            error_type=
                type(e).__name__,
            message=str(e),
        )

        raise

def service_node(
    state: MultiAgentState
):

    request_id = state["request_id"]

    start = perf_counter()

    print(
        "\n[Service Agent] Start"
    )


    log_event(
        request_id,
        "node_start",
        node="service",
    )


    try:

        shared_context = (
            state.get(
                "order_context",
                ""
            )
        )


        # =================================
        # 执行 Service Agent
        # =================================

        detail = (
            run_service_agent_detailed(
                state["user_query"],
                shared_context=
                    shared_context,
            )
        )


        answer = detail["answer"]


        # =================================
        # 统计 Tool
        # =================================

        tools = (
            state.get(
                "tool_calls",
                []
            )
            + detail["tool_names"]
        )


        for tool_name in (
            detail["tool_names"]
        ):

            log_event(
                request_id,
                "tool_used",
                agent="service",
                tool=tool_name,
            )


        # =================================
        # 统计耗时
        # =================================

        latency_ms = (
            perf_counter()
            - start
        ) * 1000


        latencies = dict(
            state.get(
                "node_latencies",
                {}
            )
        )

        latencies[
            "service"
        ] = latency_ms


        # =================================
        # Visited Agents
        # =================================

        visited = (
            state.get(
                "visited_agents",
                []
            )
            + ["service"]
        )


        log_event(
            request_id,
            "agent_end",
            agent="service",
            latency_ms=latency_ms,
            llm_calls=
                detail["llm_calls"],
        )


        # =================================
        # 写回 State
        # =================================

        return {

            "current_agent":
                "service",

            "agent_result":
                answer,

            "final_answer":
                answer,

            "visited_agents":
                visited,

            "tool_calls":
                tools,

            "llm_calls":
                state.get(
                    "llm_calls",
                    0
                )
                + detail[
                    "llm_calls"
                ],

            "node_latencies":
                latencies,
        }


    except Exception as e:

        log_event(
            request_id,
            "error",
            node="service",
            error_type=
                type(e).__name__,
            message=str(e),
        )

        raise

def route_from_supervisor(
    state: MultiAgentState
):

    return state["route"]

def route_after_order(
    state: MultiAgentState
):

    return state.get(
        "handoff_to",
        "end"
    )

builder = StateGraph(
    MultiAgentState
)


builder.add_node(
    "supervisor",
    supervisor_node,
)

builder.add_node(
    "product_agent",
    product_node,
)

builder.add_node(
    "order_agent",
    order_node,
)

builder.add_node(
    "service_agent",
    service_node,
)

builder.add_edge(
    START,
    "supervisor",
)


builder.add_conditional_edges(
    "supervisor",

    route_from_supervisor,

    {
        "product":
            "product_agent",

        "order":
            "order_agent",

        "service":
            "service_agent",
    },
)

builder.add_conditional_edges(
    "order_agent",

    route_after_order,

    {
        "service":
            "service_agent",

        "end":
            END,
    },
)

builder.add_edge(
    "product_agent",
    END,
)

builder.add_edge(
    "service_agent",
    END,
)

observable_graph = (
    builder.compile()
)
