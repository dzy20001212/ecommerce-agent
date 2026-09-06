from app.services.chat_service import (
    chat,
)


print(
    "\n"
    "=============================="
)

print(
    "Refactored E-commerce Agent"
)

print(
    "=============================="
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


    result = chat(
        question
    )


    print(
        "\nRoute:",
        result["route"]
    )

    print(
        "Agents:",
        result["agents"]
    )

    print(
        "Tools:",
        result["tools"]
    )

    print(
        "LLM Calls:",
        result["llm_calls"]
    )

    print(
        "Handoff:",
        result[
            "handoff_count"
        ]
    )

    print(
        f"Latency: "
        f"{result['latency_ms']:.2f} ms"
    )

    print(
        "\nAnswer:"
    )

    print(
        result["answer"]
    )