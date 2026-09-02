from multi_agent.graph_handoff import (
    handoff_graph,
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


    result = (
        handoff_graph.invoke(
            {
                "user_query":
                    question
            }
        )
    )


    print(
        "\nInitial Route:",
        result.get(
            "initial_route"
        )
    )

    print(
        "Visited Agents:",
        result.get(
            "visited_agents"
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
        "Handoff Reason:",
        result.get(
            "handoff_reason",
            ""
        )
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