# Week 5 Day 3 - Ecommerce Agent V1

## 1. 今日目标

构建完整的电商客服 Agent V1。


## 2. System Architecture

User
→ LLM Agent
→ Tool Calling

Tools:

- search_product
- query_order
- query_logistics
- search_policy
- transfer_to_human


## 3. Data Layer

products.json

orders.json

logistics.json

policies.json


## 4. Agent Flow

User
→ Model
→ Tool Call
→ Tool Result
→ Model
→ Final Answer


## 5. Multi-step Tool Calling

Question:

订单10001里的商品支持主动降噪吗？

Actual:

填写实际执行轨迹


## 6. Test Result

总测试数量：

10

成功数量：

10

Task Success Rate：

100%


## 7. Bad Cases

目前没有不好的用例


## 8. Summary

完成电商客服 Agent V1，
实现商品、订单、物流、
售后和人工客服等基础业务能力。