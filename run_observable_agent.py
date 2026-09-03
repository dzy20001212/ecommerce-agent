from time import perf_counter

from multi_agent.graph_observable import (
    observable_graph,
)

from observability.tracer import (
    new_request_id,
    log_event,
)


while True:

    question = input(
        "\nUser: "
    ).strip()


    if question.lower() in {
        "exit",
        "quit",
    }:

        break


    request_id = (
        new_request_id()
    )


    print(
        "\nRequest ID:",
        request_id
    )


    log_event(
        request_id,
        "request_start",
        query=question,
    )


    start = perf_counter()


    try:

        result = (
            observable_graph.invoke(
                {
                    "user_query":
                        question,

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
        )


        total_latency_ms = (
            perf_counter()
            - start
        ) * 1000


        log_event(
            request_id,
            "request_end",
            total_latency_ms=
                total_latency_ms,

            route=
                result.get(
                    "initial_route"
                ),

            visited_agents=
                result.get(
                    "visited_agents",
                    []
                ),

            tool_calls=
                result.get(
                    "tool_calls",
                    []
                ),

            llm_calls=
                result.get(
                    "llm_calls",
                    0
                ),

            handoff_count=
                result.get(
                    "handoff_count",
                    0
                ),
        )


        print(
            "\n=========================="
        )

        print(
            "Observability"
        )

        print(
            "=========================="
        )


        print(
            "Route:",
            result.get(
                "initial_route"
            )
        )

        print(
            "Visited Agents:",
            result.get(
                "visited_agents",
                []
            )
        )

        print(
            "Tools:",
            result.get(
                "tool_calls",
                []
            )
        )

        print(
            "LLM Calls:",
            result.get(
                "llm_calls",
                0
            )
        )

        print(
            "Handoff Count:",
            result.get(
                "handoff_count",
                0
            )
        )

        print(
            "Node Latencies:",
            result.get(
                "node_latencies",
                {}
            )
        )

        print(
            f"Total Latency: "
            f"{total_latency_ms:.2f} ms"
        )

        print(
            "\nFinal Answer:"
        )

        print(
            result.get(
                "final_answer",
                ""
            )
        )


    except Exception as e:

        total_latency_ms = (
            perf_counter()
            - start
        ) * 1000


        log_event(
            request_id,
            "request_error",
            error_type=
                type(e).__name__,
            message=str(e),
            total_latency_ms=
                total_latency_ms,
        )


        print(
            "\nRequest Failed:"
        )

        print(e)