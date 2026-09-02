# Week 7 Day 1 - Multi-Agent Architecture Design

## 1. Goal

将第五、六周完成的单 Agent 电商客服系统，
升级为 Supervisor + Worker Agent 的 Multi-Agent 架构。

---

## 2. Existing Capabilities

保留原有能力：

- LangChain
- LangGraph
- Tool Calling
- Memory
- Redis Cache
- Context Trim
- Summary
- Retry
- Backoff
- Fallback
- Permission
- Input Guard
- Sensitive Data Masking
- Evaluation

---

## 3. Multi-Agent Architecture

User
↓
Supervisor
↓
Product / Order / Service Agent
↓
Business Tools
↓
Final Answer

---

## 4. Supervisor

Responsibilities:

- Intent recognition
- Agent routing
- Task coordination

Supervisor does not directly execute business Tools.

---

## 5. Product Agent

Responsibilities:

- Product information
- Product price
- Product capability

Tools:

- search_product

---

## 6. Order Agent

Responsibilities:

- Order information
- Order status
- Logistics

Tools:

- query_order
- query_logistics

---

## 7. Service Agent

Responsibilities:

- Refund
- Return
- Exchange
- Human service

Tools:

- search_policy
- transfer_to_human

---

## 8. Routing

product:
商品相关问题

order:
订单和物流相关问题

service:
售后及人工客服相关问题

---

## 9. Shared State

主要保存：

- user_query
- route
- current_agent
- order_id
- product_name
- tool_result
- agent_result
- final_answer

---

## 10. Day 1 Result

完成：

- Agent职责划分
- Tool能力划分
- Routing设计
- Shared State设计
- Routing测试集

Day 2将正式实现Supervisor与Worker Agent。