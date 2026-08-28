# Week 6 Day 3 - Agent Reliability

## 1. Goal

为电商客服 Agent 增加 Retry、
Timeout、Fallback 和 Error Handling，
提高外部服务异常情况下的系统稳定性。


## 2. Error Types

Retryable:

- TimeoutError
- ConnectionError


Non-Retryable:

- 参数错误
- 业务数据不存在
- 权限问题


## 3. LLM Reliability

Model:

DeepSeek

Timeout:

30 seconds

Max Retries:

2


## 4. Tool Retry Strategy

search_product:
2 attempts

query_order:
2 attempts

query_logistics:
3 attempts

search_policy:
2 attempts

transfer_to_human:
1 attempt


## 5. Retry Test

Scenario:

query_logistics 前2次 Timeout，
第3次成功。

Expected:

Retries = 2
Fallback = 0

Actual:

填写实际结果

Result:

PASS / FAIL


## 6. Fallback Test

Scenario:

query_logistics 连续失败超过
最大重试次数。

Expected:

Tool Failures = 1
Fallback Count = 1
Agent不崩溃

Actual:

填写真实结果

Result:

PASS / FAIL


## 7. Business Error Test

Question:

订单99999发货了吗？

Expected:

不进行Retry。

Actual:

填写真实结果


## 8. Action Tool

transfer_to_human 不进行自动Retry，
避免产生重复副作用。


## 9. Metrics

Tool Retries:

填写

Tool Failures:

填写

Fallback Count:

填写


## 10. Bad Cases

填写真实问题。


## 11. Summary

通过 Timeout、Retry、Backoff 和
Fallback 机制，提高 Agent 在 LLM
和业务 Tool 临时异常情况下的容错能力。