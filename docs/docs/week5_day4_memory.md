# Week 5 Day 4 - Agent Memory

## 1. 今日目标

实现 Agent Short-term Memory，
支持同一会话中的多轮上下文理解。


## 2. Core Concepts

Short-term Memory

Agent State

Checkpointer

Thread

thread_id


## 3. Memory Flow

User Message
→ Agent
→ State
→ Checkpointer
→ thread_id

Next User Message
→ Same thread_id
→ Load State
→ Agent


## 4. Implementation

Checkpointer:

InMemorySaver

Thread Config:

{
    "configurable": {
        "thread_id": "customer_001"
    }
}


## 5. Multi-turn Test

Turn 1:

我的订单号是10001

Turn 2:

它发货了吗？

Actual Tool:

填写真实结果

Result:

PASS / FAIL


Turn 3:

那快递到哪里了？

Actual Tool:

填写真实结果

Result:

PASS / FAIL


## 6. Thread Isolation

Thread A:

订单10001

Thread B:

它发货了吗？

Actual:

填写真实结果

Result:

PASS / FAIL


## 7. Bad Cases
无问题


## 8. Limitation

InMemorySaver 保存在内存中，
程序重启后历史会丢失。


## 9. Summary

完成 Agent 短期记忆，
实现 thread 级多轮对话和会话隔离。