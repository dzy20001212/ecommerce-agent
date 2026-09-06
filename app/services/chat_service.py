from time import perf_counter

from app.graphs.multi_agent_graph import (
    multi_agent_graph,
)

from app.observability.tracer import (
    new_request_id,
)


def chat(
    message: str
) -> dict:

    request_id = new_request_id()

    start = perf_counter()


    result = multi_agent_graph.invoke(
        {
            "user_query":
                message,

            "request_id":
                request_id,

            "tool_calls":
                [],

            "llm_calls":
                0,

            "node_latencies":
                {},

            "errors":
                [],

            "visited_agents":
                [],

            "handoff_count":
                0,
        }
    )


    latency_ms = (
        perf_counter()
        - start
    ) * 1000


    return {

        "request_id":
            request_id,

        "answer":
            result.get(
                "final_answer",
                ""
            ),

        "route":
            result.get(
                "initial_route"
            ),

        "agents":
            result.get(
                "visited_agents",
                []
            ),

        "tools":
            result.get(
                "tool_calls",
                []
            ),

        "llm_calls":
            result.get(
                "llm_calls",
                0
            ),

        "handoff_count":
            result.get(
                "handoff_count",
                0
            ),

        "latency_ms":
            latency_ms,
    }