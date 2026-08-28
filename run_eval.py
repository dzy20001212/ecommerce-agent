import json
from pathlib import Path

from services.secure_agent import (
    ask_secure_agent
)

from eval.evaluator import (
    extract_tool_calls,
    evaluate_case,
)

BASE_DIR = Path(
    __file__
).resolve().parent


TEST_CASE_FILE = (
    BASE_DIR
    / "eval"
    / "test_cases.json"
)


RESULT_FILE = (
    BASE_DIR
    / "eval"
    / "results.json"
)

with open(
    TEST_CASE_FILE,
    "r",
    encoding="utf-8",
) as f:

    test_cases = json.load(f)

results = []


for index, case in enumerate(
    test_cases,
    start=1,
):

    print(
        "\n"
        "================================="
    )

    print(
        f"Case {index}: "
        f"{case['id']}"
    )

    print(
        "Question:",
        case["question"]
    )


    # 每条Case使用独立Thread
    # 避免Memory相互污染

    thread_id = (
        f"eval_{case['id']}"
    )


    actual = ask_secure_agent(
        case["question"],
        thread_id,
    )


    actual["tool_calls"] = (
        extract_tool_calls(
            actual.get(
                "messages",
                []
            )
        )
    )


    evaluation = (
        evaluate_case(
            case,
            actual,
        )
    )


    results.append(
        evaluation
    )


    print(
        "Expected Tool:",
        evaluation[
            "expected_tool"
        ]
    )


    print(
        "Actual Tool:",
        evaluation[
            "actual_tool"
        ]
    )


    print(
        "Tool Correct:",
        evaluation[
            "tool_correct"
        ]
    )


    print(
        "Args Correct:",
        evaluation[
            "args_correct"
        ]
    )


    print(
        "Answer Correct:",
        evaluation[
            "answer_correct"
        ]
    )


    print(
        "Security Correct:",
        evaluation[
            "block_correct"
        ]
    )


    print(
        "PASS:",
        evaluation[
            "passed"
        ]
    )


total = len(results)


tool_cases = [
    r
    for r in results
    if r["expected_tool"]
    is not None
]


tool_correct_count = sum(
    1
    for r in tool_cases
    if r["tool_correct"]
)


tool_accuracy = (
    tool_correct_count
    / len(tool_cases)
    if tool_cases
    else 0
)


args_correct_count = sum(
    1
    for r in tool_cases
    if r["args_correct"]
)


args_accuracy = (
    args_correct_count
    / len(tool_cases)
    if tool_cases
    else 0
)


answer_correct_count = sum(
    1
    for r in results
    if r["answer_correct"]
)


answer_accuracy = (
    answer_correct_count
    / total
    if total
    else 0
)

security_cases = [
    r
    for r in results
    if r["category"]
    == "security"
]


security_correct = sum(
    1
    for r in security_cases
    if r["block_correct"]
)


security_accuracy = (
    security_correct
    / len(security_cases)
    if security_cases
    else 0
)

passed_count = sum(
    1
    for r in results
    if r["passed"]
)


task_success_rate = (
    passed_count
    / total
    if total
    else 0
)

print(
    "\n\n"
    "================================="
)

print(
    "Evaluation Summary"
)

print(
    "================================="
)


print(
    f"Total Cases: "
    f"{total}"
)


print(
    f"Passed: "
    f"{passed_count}"
)


print(
    f"Task Success Rate: "
    f"{task_success_rate:.2%}"
)


print(
    f"Tool Selection Accuracy: "
    f"{tool_accuracy:.2%}"
)


print(
    f"Tool Argument Accuracy: "
    f"{args_accuracy:.2%}"
)


print(
    f"Answer Accuracy: "
    f"{answer_accuracy:.2%}"
)


print(
    f"Security Accuracy: "
    f"{security_accuracy:.2%}"
)

report = {

    "summary": {

        "total_cases":
            total,

        "passed":
            passed_count,

        "task_success_rate":
            task_success_rate,

        "tool_selection_accuracy":
            tool_accuracy,

        "tool_argument_accuracy":
            args_accuracy,

        "answer_accuracy":
            answer_accuracy,

        "security_accuracy":
            security_accuracy,
    },

    "results":
        results,
}

with open(
    RESULT_FILE,
    "w",
    encoding="utf-8",
) as f:

    json.dump(
        report,
        f,
        ensure_ascii=False,
        indent=2,
    )
