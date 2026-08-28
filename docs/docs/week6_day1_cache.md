# Week 6 Day 1 - Redis Cache & Performance

## 1. 今日目标

为电商客服 Agent 增加 Redis 缓存，
降低重复静态请求的响应时间和 LLM 调用次数。


## 2. Architecture

User
→ Redis Cache

Cache Hit:
→ Cached Answer

Cache Miss:
→ LangGraph Agent
→ LLM
→ Tool
→ LLM
→ Final Answer
→ Redis


## 3. Redis Configuration

Host:

localhost

Port:

6379

TTL:

3600 seconds


## 4. Cache Strategy

允许缓存：

- search_product
- search_policy

暂不缓存：

- query_order
- query_logistics
- transfer_to_human


## 5. Test 1 - Product Query

Question:

AirSound Pro支持主动降噪吗？

First Request:

Cache Hit:
填写真实结果

Response Time:
填写真实结果

LLM Calls:
填写真实结果


Second Request:

Cache Hit:
填写真实结果

Response Time:
填写真实结果

LLM Calls:
填写真实结果


## 6. Test 2 - Dynamic Order Query

Question:

订单10001发货了吗？

Expected:

两次都不使用 Response Cache。

Actual:

填写实际结果。


## 7. Benchmark

Requests:

5

Cache Hits:

填写真实结果

Cache Hit Rate:

填写真实结果

First Request Latency:

填写真实结果

Average Cached Latency:

填写真实结果


## 8. Redis Failure Test

Redis停止后：

Agent是否仍可以运行：

PASS / FAIL


## 9. Bad Cases

记录真实问题。


## 10. Summary

完成 Redis Response Cache，
对商品和售后等静态请求进行缓存，
并通过 Response Time、LLM Calls、
Tool Calls 和 Cache Hit Rate
评估缓存效果。