from services.secure_agent import (
    ask_secure_agent,
)

from utils.reliability import (
    configure_failure_simulation,
    clear_failure_simulation,
)


print(
    "\n"
    "=================================="
)

print(
    "Reliability Test 1:"
)

print(
    "Retry -> Recovery"
)

print(
    "=================================="
)


# query_logistics最多3次Attempt
# 故意让前2次失败
# 第3次应该成功

configure_failure_simulation(
    tool_name="query_logistics",
    failures=2,
)


result = ask_secure_agent(
    "订单10001的物流到哪里了？",
    thread_id=(
        "reliability_retry_test_001"
    ),
)


print(
    "\nAnswer:",
    result["answer"]
)

print(
    "Retries:",
    result.get(
        "tool_retries",
        0
    )
)

print(
    "Failures:",
    result.get(
        "tool_failailures",
        result.get(
            "tool_failures",
            0
        )
    )
)

print(
    "Fallback:",
    result.get(
        "fallback_count",
        0
    )
)


clear_failure_simulation()

print(
    "\n"
    "=================================="
)

print(
    "Reliability Test 2:"
)

print(
    "Retry Exhausted -> Fallback"
)

print(
    "=================================="
)


# Tool最多执行3次
# 我们要求失败5次
# 所以前3次一定全部失败

configure_failure_simulation(
    tool_name="query_logistics",
    failures=5,
)


result = ask_secure_agent(
    "订单10001的物流到哪里了？",
    thread_id=(
        "reliability_fallback_test_001"
    ),
)


print(
    "\nAnswer:",
    result["answer"]
)


print(
    "Retries:",
    result.get(
        "tool_retries",
        0
    )
)


print(
    "Failures:",
    result.get(
        "tool_failures",
        0
    )
)


print(
    "Fallback:",
    result.get(
        "fallback_count",
        0
    )
)


clear_failure_simulation()

reliability_pass = (
    result.get(
        "tool_retries",
        0
    ) == 2
    and
    result.get(
        "tool_failures",
        0
    ) == 1
    and
    result.get(
        "fallback_count",
        0
    ) == 1
)


print(
    "Fallback Test PASS:",
    reliability_pass
)