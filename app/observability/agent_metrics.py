def summarize_agent_messages(
    messages
):

    tool_names = []

    llm_calls = 0


    for message in messages:

        message_type = getattr(
            message,
            "type",
            ""
        )


        # AIMessage一般代表一次模型输出
        if message_type == "ai":

            llm_calls += 1


            tool_calls = getattr(
                message,
                "tool_calls",
                []
            ) or []


            for call in tool_calls:

                if isinstance(
                    call,
                    dict
                ):

                    tool_name = (
                        call.get(
                            "name"
                        )
                    )

                else:

                    tool_name = getattr(
                        call,
                        "name",
                        None
                    )


                if tool_name:

                    tool_names.append(
                        tool_name
                    )


    if messages:

        answer = getattr(
            messages[-1],
            "content",
            ""
        )

    else:

        answer = ""


    return {
        "answer":
            answer,

        "tool_names":
            tool_names,

        "llm_calls":
            llm_calls,
    }