# Week 7 Day 3 - Shared State & Agent Handoff

## Goal

在Day 2单次Agent Routing基础上，
实现多个Worker Agent之间的任务交接。

## Architecture

Supervisor
→ Order Agent
→ Shared State
→ Service Agent
→ Final Answer

## Shared State

新增：

- order_context
- handoff_to
- handoff_reason
- handoff_count
- visited_agents

## Handoff Rule

当用户问题同时包含订单需求和售后需求时：

1. Supervisor先路由至Order Agent
2. Order Agent查询订单事实
3. 结果写入Shared State
4. Handoff至Service Agent
5. Service Agent结合订单信息查询售后政策
6. 输出最终回答

## Error Handling

如果订单不存在，
停止后续Service Agent调用。

## Evaluation

通过week7_handoff_cases.json评测：

- Agent Sequence
- Handoff Count
- Handoff Accuracy：75%