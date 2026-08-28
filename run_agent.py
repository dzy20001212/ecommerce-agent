from langchain.messages import (
    AIMessage,
    ToolMessage,
)

from agent import agent


def run_question(question: str):

    print("\n用户问题：")
    print(question)

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    print("\n===== Agent执行轨迹 =====")

    for message in result["messages"]:

        if isinstance(message, AIMessage):

            if message.tool_calls:

                for tool_call in message.tool_calls:

                    print(
                        f"\nTool Call: "
                        f"{tool_call['name']}"
                    )

                    print(
                        f"Args: "
                        f"{tool_call['args']}"
                    )

        elif isinstance(message, ToolMessage):

            print(
                f"\nTool Result: "
                f"{message.content}"
            )

    print("\n===== 最终回答 =====")

    print(
        result["messages"][-1].content
    )


if __name__ == "__main__":

    question = input(
        "请输入问题："
    )

    run_question(question)