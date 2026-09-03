# Week 7 Day 4 - Multi-Agent Observability

## Goal

为Multi-Agent系统增加运行监控能力，
记录Supervisor、Worker Agent、Tool和Handoff执行链路。

## Metrics

- Request ID
- Route
- Visited Agents
- Tool Calls
- LLM Calls
- Node Latency
- Total Latency
- Handoff Count
- Errors

## Trace

每个用户请求生成唯一Request ID，
将Supervisor、Worker、Tool和Handoff日志关联为一条完整Trace。

## Logs

日志保存至：

logs/week7_observability.jsonl

## Report

通过run_observability_report.py统计：

- 请求数量
- 平均延迟
- 平均LLM调用次数
- Route分布
- Tool使用次数
- Handoff次数
- Error数量

## Result

实现Multi-Agent基础Observability，
为后续Evaluation、性能分析和系统优化提供数据。