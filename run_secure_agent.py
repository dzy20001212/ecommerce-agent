from services.secure_agent import (
    ask_secure_agent
)


THREAD_ID = "customer_security_001"


while True:

    question = input(
        "\nUser: "
    ).strip()


    if question.lower() in {
        "quit",
        "exit",
    }:

        break


    result = ask_secure_agent(
        question,
        THREAD_ID,
    )


    print(
        "\nAgent:",
        result["answer"]
    )


    print(
        "\n--- Security Metrics ---"
    )


    print(
        "Blocked:",
        result.get(
            "blocked",
            False
        )
    )


    print(
        "Permission Denied:",
        result.get(
            "permission_denied",
            0
        )
    )


    print(
        "Security Events:",
        result.get(
            "security_events",
            0
        )
    )


    print(
        "Masked:",
        result.get(
            "masked_count",
            0
        )
    )


    print(
        "Retries:",
        result.get(
            "tool_retries",
            0
        )
    )