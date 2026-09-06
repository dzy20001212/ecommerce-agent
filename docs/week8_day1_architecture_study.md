# Week 8 Day 1 - Architecture Study

## 1. Goal

参考 WeKnora 等成熟 AI 应用项目，
学习大型 AI 系统的模块划分和工程架构，
为 ecommerce-agent 的模块化重构做准备。

## 2. WeKnora System Architecture

核心模块包括：

- Frontend
- Backend App
- Agent
- Document Service
- Database
- Redis
- Observability
- Deployment

主要思想：

不同模块按照职责进行拆分，
通过 API、服务调用以及基础设施进行协作，
而不是把全部功能写在单一模块中。