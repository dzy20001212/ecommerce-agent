import json
from pathlib import Path

from services.secure_agent import (
    ask_secure_agent,
)

from eval.evaluator import (
    extract_tool_calls,
    args_match,
)


BASE_DIR = Path(
    __file__
).resolve().parent


MEMORY_CASE_FILE = (
    BASE_DIR
    / "eval"
    / "memory_cases.json"
)


with open(
    MEMORY_CASE_FILE,
    "r",
    encoding="utf-8",
) as f:

    memory_cases = json.load(f)


total_checks = 0
passed_checks = 0


for case in memory_cases:

    print(
        "\n"
        "===================================="
    )

    print(
        "Memory Case:",
        case["id"]
    )

    print(
        "===================================="
    )


    # 同一个Memory Case中的所有轮次
    # 必须共享Thread

    thread_id = (
        f"memory_eval_{case['id']}"
    )


    for turn_index, turn in enumerate(
        case["turns"],
        start=1,
    ):

        question = turn["question"]


        print(
            f"\nTurn {turn_index}"
        )

        print(
            "Question:",
            question
        )


        actual = ask_secure_agent(
            question,
            thread_id,
        )


        print(
            "Answer:",
            actual["answer"]
        )


        # 第一轮可能只是告诉Agent订单号
        # 不一定需要Tool
        if "expected_tool" not in turn:

            print(
                "This turn does not require "
                "Tool evaluation."
            )

            continue


        total_checks += 1


        tool_calls = extract_tool_calls(
            actual.get(
                "messages",
                []
            )
        )


        # 因为同一个Thread包含以前的Tool Call
        # 所以这里一定取最后一次
        last_tool_call = (
            tool_calls[-1]
            if tool_calls
            else None
        )


        actual_tool = (
            last_tool_call["name"]
            if last_tool_call
            else None
        )


        actual_args = (
            last_tool_call["args"]
            if last_tool_call
            else {}
        )


        expected_tool = (
            turn["expected_tool"]
        )


        expected_args = (
            turn["expected_args"]
        )


        tool_correct = (
            actual_tool
            == expected_tool
        )


        arg_correct = args_match(
            expected_args,
            actual_args,
        )


        passed = (
            tool_correct
            and arg_correct
        )


        if passed:
            passed_checks += 1


        print(
            "Expected Tool:",
            expected_tool
        )

        print(
            "Actual Tool:",
            actual_tool
        )

        print(
            "Expected Args:",
            expected_args
        )

        print(
            "Actual Args:",
            actual_args
        )

        print(
            "Tool Correct:",
            tool_correct
        )

        print(
            "Args Correct:",
            arg_correct
        )

        print(
            "PASS:",
            passed
        )


memory_accuracy = (
    passed_checks / total_checks
    if total_checks
    else 0
)


print(
    "\n"
    "===================================="
)

print(
    "Memory Evaluation Summary"
)

print(
    "===================================="
)

print(
    "Total Checks:",
    total_checks
)

print(
    "Passed:",
    passed_checks
)

print(
    f"Memory Accuracy: "
    f"{memory_accuracy:.2%}"
)