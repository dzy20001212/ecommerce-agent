import json

from pathlib import Path
from time import perf_counter

from multi_agent.graph_observable import (
    observable_graph,
)

from observability.tracer import (
    new_request_id,
)

from eval.week7_evaluator import (
    evaluate_case,
)


BASE_DIR = Path(
    __file__
).resolve().parent


CASE_FILE = (
    BASE_DIR
    / "eval"
    / "week7_multi_agent_cases.json"
)


RESULT_FILE = (
    BASE_DIR
    / "eval"
    / "week7_results.json"
)


with open(
    CASE_FILE,
    "r",
    encoding="utf-8",
) as f:

    cases = json.load(f)


results = []


for case in cases:

    print(
        "\n"
        "================================="
    )

    print(
        "Case:",
        case["id"]
    )

    print(
        "Question:",
        case["question"]
    )


    request_id = (
        new_request_id()
    )


    start = perf_counter()


    try:

        graph_result = (
            observable_graph.invoke(
                {
                    "user_query":
                        case["question"],

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


        latency_ms = (
            perf_counter()
            - start
        ) * 1000


        evaluation = (
            evaluate_case(
                case,
                graph_result,
            )
        )


        evaluation[
            "latency_ms"
        ] = latency_ms


        evaluation[
            "llm_calls"
        ] = graph_result.get(
            "llm_calls",
            0
        )


        evaluation[
            "request_id"
        ] = request_id


        results.append(
            evaluation
        )


        print(
            "Route:",
            evaluation[
                "actual_route"
            ]
        )

        print(
            "Agents:",
            evaluation[
                "actual_agents"
            ]
        )

        print(
            "Tools:",
            evaluation[
                "actual_tools"
            ]
        )

        print(
            "Handoff:",
            evaluation[
                "actual_handoff_count"
            ]
        )

        print(
            "LLM Calls:",
            evaluation[
                "llm_calls"
            ]
        )

        print(
            f"Latency: "
            f"{latency_ms:.2f} ms"
        )

        print(
            "PASS:",
            evaluation[
                "passed"
            ]
        )


    except Exception as e:

        latency_ms = (
            perf_counter()
            - start
        ) * 1000


        results.append(
            {
                "id":
                    case["id"],

                "question":
                    case[
                        "question"
                    ],

                "passed":
                    False,

                "error":
                    str(e),

                "latency_ms":
                    latency_ms,

                "llm_calls":
                    0,
            }
        )


# =====================================
# 汇总指标
# =====================================

total = len(results)


def accuracy(
    field
):

    if total == 0:

        return 0.0


    return (
        sum(
            1
            for r in results
            if r.get(
                field,
                False
            )
        )
        / total
    )


route_accuracy = accuracy(
    "route_correct"
)

agent_accuracy = accuracy(
    "agent_path_correct"
)

tool_accuracy = accuracy(
    "tool_correct"
)

handoff_accuracy = accuracy(
    "handoff_correct"
)

answer_accuracy = accuracy(
    "answer_correct"
)

task_success_rate = accuracy(
    "passed"
)


avg_latency = (
    sum(
        r.get(
            "latency_ms",
            0
        )
        for r in results
    )
    / total
    if total
    else 0
)


avg_llm_calls = (
    sum(
        r.get(
            "llm_calls",
            0
        )
        for r in results
    )
    / total
    if total
    else 0
)


summary = {

    "total_cases":
        total,

    "routing_accuracy":
        route_accuracy,

    "agent_path_accuracy":
        agent_accuracy,

    "tool_accuracy":
        tool_accuracy,

    "handoff_accuracy":
        handoff_accuracy,

    "answer_accuracy":
        answer_accuracy,

    "task_success_rate":
        task_success_rate,

    "average_latency_ms":
        avg_latency,

    "average_llm_calls":
        avg_llm_calls,
}


report = {
    "summary":
        summary,

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


print(
    "\n"
    "================================="
)

print(
    "Week 7 Multi-Agent Evaluation"
)

print(
    "================================="
)


print(
    "Total Cases:",
    total
)


print(
    f"Routing Accuracy: "
    f"{route_accuracy:.2%}"
)


print(
    f"Agent Path Accuracy: "
    f"{agent_accuracy:.2%}"
)


print(
    f"Tool Accuracy: "
    f"{tool_accuracy:.2%}"
)


print(
    f"Handoff Accuracy: "
    f"{handoff_accuracy:.2%}"
)


print(
    f"Answer Accuracy: "
    f"{answer_accuracy:.2%}"
)


print(
    f"Task Success Rate: "
    f"{task_success_rate:.2%}"
)


print(
    f"Average Latency: "
    f"{avg_latency:.2f} ms"
)


print(
    f"Average LLM Calls: "
    f"{avg_llm_calls:.2f}"
)


print(
    "\nResults saved to:"
)

print(
    RESULT_FILE
)