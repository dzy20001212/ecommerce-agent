from graph_agent_secure import (
    graph_agent
)

from security.input_guard import (
    check_input_security,
)

from security.masking import (
    mask_sensitive_data,
)


def ask_secure_agent(
    question: str,
    thread_id: str,
):

    # ==================================
    # 1. Input Security
    # ==================================

    input_result = (
        check_input_security(
            question
        )
    )


    if not input_result.allowed:

        return {
            "answer": (
                "该请求未通过安全检查，"
                "无法执行。"
            ),

            "blocked": True,

            "block_reason":
                input_result.reason,

            "permission_denied": 0,

            "security_events": 1,

            "masked_count": 0,
        }


    # ==================================
    # 2. Agent
    # ==================================

    config = {

        "configurable": {

            "thread_id":
                thread_id
        }
    }


    result = graph_agent.invoke(

        {

            "messages": [

                {
                    "role": "user",
                    "content": question,
                }
            ],

            "permission_denied": 0,

            "security_events": 0,

            "tool_retries": 0,

            "tool_failures": 0,

            "fallback_count": 0,
        },

        config,
    )


    answer = (
        result["messages"][-1]
        .content
    )


    # ==================================
    # 3. Output Masking
    # ==================================

    mask_result = (
        mask_sensitive_data(
            str(answer)
        )
    )


    return {

        "answer":
            mask_result.text,

        "blocked": False,

        "block_reason": "",

        "permission_denied":
            result.get(
                "permission_denied",
                0
            ),

        "security_events":
            result.get(
                "security_events",
                0
            ),

        "masked_count":
            mask_result.masked_count,

        "tool_retries":
            result.get(
                "tool_retries",
                0
            ),

        "tool_failures":
            result.get(
                "tool_failures",
                0
            ),

        "fallback_count":
            result.get(
                "fallback_count",
                0
            ),

        "messages":
            result["messages"],


        "full_state_tokens":
            result.get(
        "full_state_tokens",
        0
    ),

        "model_context_tokens":
            result.get(
        "model_context_tokens",
        0
    ),

        "summary_calls":
            result.get(
        "summary_calls",
        0
    ),

        "summarized_count":
            result.get(
        "summarized_count",
        0
    ),
    }