import json
from pathlib import Path

from agents.supervisor import (
    decide_route,
)


BASE_DIR = Path(
    __file__
).resolve().parent


CASE_FILE = (
    BASE_DIR
    / "eval"
    / "week7_routing_cases.json"
)


with open(
    CASE_FILE,
    "r",
    encoding="utf-8",
) as f:

    cases = json.load(f)


total = len(cases)

correct = 0


for case in cases:

    actual_route = decide_route(
        case["question"]
    )


    expected_route = (
        case["expected_route"]
    )


    passed = (
        actual_route
        == expected_route
    )


    if passed:

        correct += 1


    print(
        "\nCase:",
        case["id"]
    )

    print(
        "Question:",
        case["question"]
    )

    print(
        "Expected:",
        expected_route
    )

    print(
        "Actual:",
        actual_route
    )

    print(
        "PASS:",
        passed
    )


accuracy = (
    correct / total
    if total
    else 0
)


print(
    "\n"
    "================================="
)

print(
    "Routing Evaluation"
)

print(
    "================================="
)


print(
    "Total:",
    total
)

print(
    "Correct:",
    correct
)

print(
    f"Routing Accuracy: "
    f"{accuracy:.2%}"
)