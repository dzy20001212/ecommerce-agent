def answer_match(
    answer: str,
    expected_any_keywords: list[str],
    forbidden_keywords: list[str],
) -> bool:

    answer = str(answer)


    # 先检查禁止出现的内容
    for keyword in forbidden_keywords:

        if keyword in answer:

            return False


    # 没有规定关键词时
    if not expected_any_keywords:

        return True


    # 任意一个正确关键词出现即可
    return any(
        keyword in answer
        for keyword
        in expected_any_keywords
    )


def evaluate_case(
    case: dict,
    result: dict,
):

    actual_route = result.get(
        "initial_route"
    )


    actual_agents = result.get(
        "visited_agents",
        []
    )


    actual_tools = result.get(
        "tool_calls",
        []
    )


    actual_handoff_count = (
        result.get(
            "handoff_count",
            0
        )
    )


    answer = result.get(
        "final_answer",
        ""
    )


    # =================================
    # Route
    # =================================

    route_correct = (
        actual_route
        == case[
            "expected_route"
        ]
    )


    # =================================
    # Agent执行路径
    # =================================

    agent_path_correct = (
        actual_agents
        == case[
            "expected_agents"
        ]
    )


    # =================================
    # Tool
    #
    # 只要求期望Tool都被调用，
    # 不强制实际列表完全相等
    # =================================

    tool_correct = all(
        tool in actual_tools
        for tool
        in case[
            "expected_tools"
        ]
    )


    # =================================
    # Handoff
    # =================================

    handoff_correct = (
        actual_handoff_count
        == case[
            "expected_handoff_count"
        ]
    )


    # =================================
    # Answer
    # =================================

    answer_correct = answer_match(
        answer,

        case.get(
            "expected_any_keywords",
            []
        ),

        case.get(
            "forbidden_keywords",
            []
        ),
    )


    # =================================
    # 最终Pass
    # =================================

    passed = all(
        [
            route_correct,
            agent_path_correct,
            tool_correct,
            handoff_correct,
            answer_correct,
        ]
    )


    return {

        "id":
            case["id"],

        "question":
            case["question"],

        "route_correct":
            route_correct,

        "agent_path_correct":
            agent_path_correct,

        "tool_correct":
            tool_correct,

        "handoff_correct":
            handoff_correct,

        "answer_correct":
            answer_correct,

        "passed":
            passed,

        "expected_route":
            case["expected_route"],

        "actual_route":
            actual_route,

        "expected_agents":
            case["expected_agents"],

        "actual_agents":
            actual_agents,

        "expected_tools":
            case["expected_tools"],

        "actual_tools":
            actual_tools,

        "expected_handoff_count":
            case[
                "expected_handoff_count"
            ],

        "actual_handoff_count":
            actual_handoff_count,

        "answer":
            answer,
    }