# Week 8 Day 3 - FastAPI Service

## Goal

将 ecommerce-agent 从本地 Python 脚本
升级为可通过 HTTP API 调用的后端服务。

## Architecture

Client
→ HTTP Request
→ FastAPI
→ Chat Service
→ Multi-Agent Graph
→ Worker Agent
→ Tool
→ HTTP Response

## APIs

### GET /health

用于检查Agent服务是否正常运行。

### POST /chat

Request:

{
  "message": "查询订单10001"
}

Response:

- request_id
- answer
- route
- agents
- tools
- llm_calls
- handoff_count
- latency_ms

## Validation

完成：

- Product Agent API调用
- Order Agent API调用
- Service Agent API调用
- Multi-Agent Handoff API调用
- Swagger测试
- Health Check