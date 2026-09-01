from multi_agent.graph import (
    multi_agent_graph,
)


print(
    "\n"
    "================================="
)

print(
    "E-commerce Multi-Agent"
)

print(
    "================================="
)


while True:

    question = input(
        "\nUser: "
    ).strip()


    if question.lower() in {
        "quit",
        "exit",
    }:

        break


    result = (
        multi_agent_graph.invoke(
            {
                "user_query":
                    question
            }
        )
    )


    print(
        "\nRoute:",
        result.get(
            "route"
        )
    )


    print(
        "Agent:",
        result.get(
            "current_agent"
        )
    )


    print(
        "\nAnswer:"
    )

    print(
        result.get(
            "final_answer",
            ""
        )
    )