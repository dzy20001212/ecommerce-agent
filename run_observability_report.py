import json

from collections import Counter
from pathlib import Path


BASE_DIR = Path(
    __file__
).resolve().parent


LOG_FILE = (
    BASE_DIR
    / "logs"
    / "week7_observability.jsonl"
)


if not LOG_FILE.exists():

    print(
        "No observability log found."
    )

    raise SystemExit


events = []


with open(
    LOG_FILE,
    "r",
    encoding="utf-8",
) as f:

    for line in f:

        line = line.strip()

        if not line:
            continue

        events.append(
            json.loads(line)
        )


requests = [
    event
    for event in events
    if event.get("event")
    == "request_end"
]


if not requests:

    print(
        "No completed requests."
    )

    raise SystemExit


total_requests = len(
    requests
)


average_latency = (
    sum(
        r.get(
            "total_latency_ms",
            0
        )
        for r in requests
    )
    / total_requests
)


average_llm_calls = (
    sum(
        r.get(
            "llm_calls",
            0
        )
        for r in requests
    )
    / total_requests
)


route_counter = Counter(
    r.get(
        "route",
        "unknown"
    )
    for r in requests
)


tool_counter = Counter()


for request in requests:

    for tool in request.get(
        "tool_calls",
        []
    ):

        tool_counter[
            tool
        ] += 1


handoff_total = sum(
    r.get(
        "handoff_count",
        0
    )
    for r in requests
)


error_count = sum(
    1
    for event in events
    if event.get(
        "event"
    ) in {
        "error",
        "request_error",
    }
)


print(
    "\n=============================="
)

print(
    "Week 7 Observability Report"
)

print(
    "=============================="
)


print(
    "Request Count:",
    total_requests
)


print(
    f"Average Latency: "
    f"{average_latency:.2f} ms"
)


print(
    f"Average LLM Calls: "
    f"{average_llm_calls:.2f}"
)


print(
    "Total Handoffs:",
    handoff_total
)


print(
    "Errors:",
    error_count
)


print(
    "\nRoute Distribution:"
)


for route, count in (
    route_counter.items()
):

    print(
        f"- {route}: {count}"
    )


print(
    "\nTool Usage:"
)


for tool, count in (
    tool_counter.items()
):

    print(
        f"- {tool}: {count}"
    )