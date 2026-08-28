from graph_agent_reliable import (
    graph_agent
)

from utils.reliability import (
    configure_failure_simulation,
    clear_failure_simulation,
)


print(
    "\n"
    "======================================"
)

print(
    "Test：Retry Exhausted -> Fallback"
)

print(
    "======================================\n"
)


# =====================================
# query_logistics最多只允许执行3次
#
# 这里要求模拟失败5次
#
# 所以：
# Attempt 1 → Failure
# Attempt 2 → Failure
# Attempt 3 → Failure
#
# 然后必须Fallback
# =====================================

configure_failure_simulation(
    tool_name="query_logistics",
    failures=5,
)


config = {

    "configurable": {

        # 每次换一个新的thread
        # 避免旧State干扰
        "thread_id":
            "retry_fallback_test_001"
    }
}


result = graph_agent.invoke(

    {

        "messages": [

            {

                "role": "user",

                "content":
                    "订单10001的物流到哪里了？",
            }
        ],


        "llm_calls": 0,

        "summary_calls": 0,

        "tool_retries": 0,

        "tool_failures": 0,

        "fallback_count": 0,

        "last_error": "",
    },

    config,
)


print(
    "\n"
    "======================================"
)

print(
    "Final Result"
)

print(
    "======================================"
)


print(
    "\nAnswer:"
)

print(
    result["messages"][-1].content
)


print(
    "\nRetries:",
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


print(
    "Last Error:",
    result.get(
        "last_error",
        ""
    )
)


# 一定必须放在invoke之后
clear_failure_simulation()