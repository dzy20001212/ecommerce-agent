from agent import agent


def ask(thread_id, question):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

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

    print("=" * 60)
    print("Thread:", thread_id)
    print("Question:", question)
    print("Answer:", result["messages"][-1].content)

    return result


print("\n===== Test 1：同一 Thread Memory =====")

ask(
    "customer_A",
    "我的订单号是10001"
)

ask(
    "customer_A",
    "它发货了吗？"
)

print("\n===== Test 2：不同 Thread 隔离 =====")

ask(
    "customer_B",
    "它发货了吗？"
)


print("\n===== Test 3：缺失上下文 =====")

ask(
    "customer_C",
    "它现在到哪里了？"
)

print("\n===== Test 4：利用历史 Tool Result =====")

ask(
    "customer_D",
    "订单10001买了什么商品？"
)

ask(
    "customer_D",
    "它支持主动降噪吗？"
)