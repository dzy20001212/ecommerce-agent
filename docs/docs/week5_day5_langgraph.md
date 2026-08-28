# Week 5 Day 5 - LangGraph Agent Workflow

## 1. 今日目标

使用 LangGraph StateGraph
手动构建电商客服 Agent Loop。


## 2. Core Concepts

State

Node

Edge

Conditional Edge

START

END

compile

Checkpointer


## 3. Graph Structure

START
→ llm_call
→ should_continue

如果存在 Tool Call：

tool_node
→ llm_call

如果不存在 Tool Call：

END


## 4. State

messages:
保存当前会话消息、Tool Call 和 Tool Result。

llm_calls:
记录模型调用次数。


## 5. Nodes

llm_call:

负责调用 LLM，
判断是否需要 Tool。


tool_node:

负责真正执行 Tool。


## 6. Conditional Edge

should_continue:

如果 AIMessage 存在 tool_calls：

→ tool_node

否则：

→ END


## 7. Multi-step Test

Question:

订单10001里的商品支持主动降噪吗？

Expected:

llm_call
→ query_order
→ llm_call
→ search_product
→ llm_call
→ END

Actual:

填写实际结果


Result:

PASS / FAIL


## 8. Memory Test

Thread:

graph_customer_001

Turn 1:

我的订单号是10001

Turn 2:

它发货了吗？

Result:

PASS / FAIL


## 9. Bad Cases




## 10. Summary

使用 StateGraph 显式构建
Model → Tool → Model Agent Loop，
理解 State、Node、Edge 和
Conditional Edge 的作用。