from agent import agent


THREAD_ID = "customer_001"


config = {
    "configurable": {
        "thread_id": THREAD_ID
    }
}


while True:

    question = input("\n用户：")

    if question.lower() in [
        "exit",
        "quit"
    ]:
        print("会话结束。")
        break


    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },
        config
    )


    answer = result["messages"][-1].content


    print("\nAgent：")
    print(answer)
