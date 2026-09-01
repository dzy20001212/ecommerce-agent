from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from multi_agent.state import (
    MultiAgentState,
)

from agents.supervisor import (
    decide_route,
)

from agents.product_agent import (
    run_product_agent,
)

from agents.order_agent import (
    run_order_agent,
)

from agents.service_agent import (
    run_service_agent,
)

def supervisor_node(
    state: MultiAgentState
):

    user_query = (
        state["user_query"]
    )


    route = decide_route(
        user_query
    )


    print(
        f"\n[Supervisor] "
        f"query={user_query}"
    )

    print(
        f"[Supervisor] "
        f"route={route}"
    )


    return {
        "route": route,
    }

def product_node(
    state: MultiAgentState
):

    print(
        "\n[Product Agent] Start"
    )


    answer = run_product_agent(
        state["user_query"]
    )


    return {

        "current_agent":
            "product",

        "agent_result":
            answer,

        "final_answer":
            answer,
    }

def order_node(
    state: MultiAgentState
):

    print(
        "\n[Order Agent] Start"
    )


    answer = run_order_agent(
        state["user_query"]
    )


    return {

        "current_agent":
            "order",

        "agent_result":
            answer,

        "final_answer":
            answer,
    }

def service_node(
    state: MultiAgentState
):

    print(
        "\n[Service Agent] Start"
    )


    answer = run_service_agent(
        state["user_query"]
    )


    return {

        "current_agent":
            "service",

        "agent_result":
            answer,

        "final_answer":
            answer,
    }

def route_worker(
    state: MultiAgentState
):

    return state["route"]

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

    route_worker,

    {
        "product":
            "product_agent",

        "order":
            "order_agent",

        "service":
            "service_agent",
    },
)

builder.add_edge(
    "product_agent",
    END,
)

builder.add_edge(
    "order_agent",
    END,
)

builder.add_edge(
    "service_agent",
    END,
)

multi_agent_graph = (
    builder.compile()
)
