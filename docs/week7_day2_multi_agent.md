# Week 7 Day 2 - Multi-Agent Implementation

## 1. Goal

实现 Supervisor + Product / Order / Service Worker Agent，
并通过 LangGraph Conditional Edge 完成动态路由。

## 2. Architecture

START
→ Supervisor
→ Routing
→ Product / Order / Service
→ END

## 3. Supervisor

负责：

- 用户意图识别
- Agent选择
- Route生成

Route：

- product
- order
- service

## 4. Worker Agents

Product Agent:
- search_product

Order Agent:
- query_order
- query_logistics

Service Agent:
- search_policy
- transfer_to_human

## 5. LangGraph

使用：

- StateGraph
- Node
- Edge
- Conditional Edge

完成Supervisor到Worker Agent的动态路由。

## 6. Evaluation

使用week7_routing_cases.json测试Supervisor Routing Accuracy。

## 7. Current Limitation

当前每次请求只路由到一个Worker Agent，
暂未实现跨Agent Handoff。

Day 3将加入Shared State和Agent Handoff。