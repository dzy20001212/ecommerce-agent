def extract_tool_calls(
    messages
):

    tool_calls = []

    for message in messages:

        calls = getattr(
            message,
            "tool_calls",
            None
        )

        if not calls:
            continue

        for call in calls:

            tool_calls.append(
                {
                    "name": call.get(
                        "name"
                    ),

                    "args": call.get(
                        "args",
                        {}
                    ),
                }
            )

    return tool_calls

def args_match(
    expected_args,
    actual_args,
) -> bool:

    if expected_args is None:
        return True

    if actual_args is None:
        return False

    for key, value in (
        expected_args.items()
    ):

        if (
            str(actual_args.get(key))
            != str(value)
        ):

            return False

    return True

def keywords_match(
    expected_keywords,
    answer: str,
) -> bool:

    if not expected_keywords:
        return True

    answer = str(answer)

    return all(
        keyword in answer
        for keyword
        in expected_keywords
    )

def evaluate_case(
    case,
    actual,
):

    tool_calls = actual.get(
        "tool_calls",
        []
    )

    first_tool_call = (
        tool_calls[0]
        if tool_calls
        else None
    )


    actual_tool = (
        first_tool_call.get("name")
        if first_tool_call
        else None
    )


    actual_args = (
        first_tool_call.get("args", {})
        if first_tool_call
        else {}
    )


    expected_tool = case.get(
        "expected_tool"
    )


    expected_args = case.get(
        "expected_args"
    )


    # =========================
    # Tool Selection
    # =========================

    tool_correct = (
        actual_tool
        == expected_tool
    )


    # 如果本来就不需要Tool
    if expected_tool is None:

        tool_correct = (
            actual_tool is None
        )


    # =========================
    # Args
    # =========================

    args_correct = (
        args_match(
            expected_args,
            actual_args,
        )
    )


    # =========================
    # Answer
    # =========================

    answer_correct = (
        keywords_match(
            case.get(
                "expected_keywords",
                []
            ),

            actual.get(
                "answer",
                ""
            ),
        )
    )


    # =========================
    # Security
    # =========================

    block_correct = (
        actual.get(
            "blocked",
            False
        )
        ==
        case.get(
            "should_block",
            False
        )
    )


    # =========================
    # Overall
    # =========================

    passed = all(
        [
            tool_correct,
            args_correct,
            answer_correct,
            block_correct,
        ]
    )


    return {

        "id":
            case["id"],

        "category":
            case["category"],

        "tool_correct":
            tool_correct,

        "args_correct":
            args_correct,

        "answer_correct":
            answer_correct,

        "block_correct":
            block_correct,

        "passed":
            passed,

        "expected_tool":
            expected_tool,

        "actual_tool":
            actual_tool,

        "expected_args":
            expected_args,

        "actual_args":
            actual_args,

        "answer":
            actual.get(
                "answer",
                ""
            ),
    }

