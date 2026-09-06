# Week 8 Day 2 - Modular Refactoring

## Goal

将 ecommerce-agent 从分散脚本结构，
重构为 app/ 分层工程结构。

## Layers

### Service

负责业务入口和Graph调用。

### Graph

负责：

- State
- Routing
- Handoff
- Multi-Agent Workflow

### Agent

负责：

- LLM
- Prompt
- Tool Calling

### Tool

负责具体业务能力。

### Infrastructure

包括：

- Redis
- Security
- Observability

## Refactor Result

完成：

- app/agents
- app/graphs
- app/tools
- app/services
- app/cache
- app/security
- app/observability

## Validation

通过Smoke Test确认：

- Product Routing
- Order Routing
- Service Routing

重构前后主要业务行为保持一致。