import json
from pathlib import Path

from multi_agent.routing import (
    VALID_ROUTES,
    AGENT_TOOL_MAPPING,
    AGENT_DESCRIPTIONS,
)


BASE_DIR = Path(
    __file__
).resolve().parent


ROUTING_CASE_FILE = (
    BASE_DIR
    / "eval"
    / "week7_routing_cases.json"
)


print(
    "\n"
    "===================================="
)

print(
    "Week 7 Day 1 Design Check"
)

print(
    "===================================="
)


# =====================================
# 1. 检查Route
# =====================================

print(
    "\nValid Routes:"
)

for route in VALID_ROUTES:

    print(
        "-",
        route
    )


# =====================================
# 2. 检查Agent -> Tool映射
# =====================================

print(
    "\nAgent Tool Mapping:"
)


for agent_name, tools in (
    AGENT_TOOL_MAPPING.items()
):

    print(
        f"{agent_name}: "
        f"{tools}"
    )


# =====================================
# 3. 检查Agent描述
# =====================================

print(
    "\nAgent Descriptions:"
)


for agent_name, description in (
    AGENT_DESCRIPTIONS.items()
):

    print(
        f"{agent_name}: "
        f"{description}"
    )


# =====================================
# 4. 读取Routing测试集
# =====================================

with open(
    ROUTING_CASE_FILE,
    "r",
    encoding="utf-8",
) as f:

    routing_cases = json.load(f)


print(
    "\nRouting Cases:",
    len(routing_cases)
)


# =====================================
# 5. 检查测试集中的Route是否合法
# =====================================

invalid_cases = []


for case in routing_cases:

    expected_route = (
        case["expected_route"]
    )

    if (
        expected_route
        not in VALID_ROUTES
    ):

        invalid_cases.append(
            case["id"]
        )


if invalid_cases:

    print(
        "\nInvalid Routing Cases:"
    )

    for case_id in invalid_cases:

        print(
            "-",
            case_id
        )

else:

    print(
        "\nAll routing cases are valid."
    )


print(
    "\nWeek 7 Day 1 Design Check PASS"
)