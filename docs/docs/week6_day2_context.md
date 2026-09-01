# Week 6 Day 2 - Context & Token Optimization

## 1. Goal

优化电商客服 Agent 多轮会话 Context，
降低发送给 LLM 的历史 Token 数量。


## 2. Problem

随着对话轮数增加：

Messages增加
→ Input Token增加
→ Latency增加
→ API Cost增加


## 3. Strategy

完整历史：

LangGraph State

模型上下文：

System Prompt
+
History Summary
+
Recent Messages


## 4. Context Trimming

Strategy:

last

Max Context Tokens:

填写实际值


## 5. Summarization

Trigger Tokens:

填写实际值

Keep Recent Messages:

填写实际值


## 6. Token Benchmark

Before:

Messages:
填写

Tokens:
填写


After:

Messages:
填写

Tokens:
填写


Token Reduction:

填写


## 7. Memory Test

Initial:

我的订单号是10001

Later:

这个订单现在发货了吗？

Result:

PASS / FAIL


## 8. Tool Calling Test

Question:

这个订单的物流在哪里？

Expected:

query_logistics(order_id="10001")

Actual:

填写实际结果


## 9. Bad Cases

Context Missing:

填写

Context Confusion:

填写

Tool Argument Error:

填写


## 10. Summary

通过 Context Trimming 和 History Summary
控制多轮对话的模型输入长度，
在保留关键业务上下文的同时减少
Input Token。