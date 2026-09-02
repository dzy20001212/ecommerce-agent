import json
from pathlib import Path

from multi_agent.graph_handoff import (
    handoff_graph,
)


BASE_DIR = Path(
    __file__
).resolve().parent


CASE_FILE = (
    BASE_DIR
    / "eval"
    / "week7_handoff_cases.json"
)


with open(
    CASE_FILE,
    "r",
    encoding="utf-8",
) as f:

    cases = json.load(f)


passed_count = 0


for case in cases:

    result = handoff_graph.invoke(
        {
            "user_query":
                case["question"]
        }
    )


    actual_agents = (
        result.get(
            "visited_agents",
            []
        )
    )


    actual_handoff_count = (
        result.get(
            "handoff_count",
            0
        )
    )


    agents_correct = (
        actual_agents
        == case[
            "expected_agents"
        ]
    )


    handoff_correct = (
        actual_handoff_count
        == case[
            "expected_handoff_count"
        ]
    )


    passed = (
        agents_correct
        and handoff_correct
    )


    if passed:
        passed_count += 1


    print(
        "\nCase:",
        case["id"]
    )

    print(
        "Question:",
        case["question"]
    )

    print(
        "Expected Agents:",
        case[
            "expected_agents"
        ]
    )

    print(
        "Actual Agents:",
        actual_agents
    )

    print(
        "Expected Handoff:",
        case[
            "expected_handoff_count"
        ]
    )

    print(
        "Actual Handoff:",
        actual_handoff_count
    )

    print(
        "PASS:",
        passed
    )


total = len(cases)


accuracy = (
    passed_count / total
    if total
    else 0
)


print(
    "\n=========================="
)

print(
    "Handoff Evaluation"
)

print(
    "=========================="
)

print(
    "Total:",
    total
)

print(
    "Passed:",
    passed_count
)

print(
    f"Handoff Accuracy: "
    f"{accuracy:.2%}"
)