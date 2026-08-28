## Bad Case Analysis

### Bad Case 1

Question:
查询订单99999

Expected Tool:
query_order

Actual Tool:
query_order

Expected Args:
{"order_id": "99999"}

Actual Args:
{"order_id": "99999"}

Expected Answer:
表达订单不存在 / 未找到

Actual Answer:
填写实际Agent回答

Error Type:
Answer Evaluation Error

Root Cause:
关键词规则只能匹配“未找到”，
但Agent可能使用“没有查询到”等同义表达。

Fix:
增加多个可接受表达，
或后续引入LLM-as-a-Judge。

Re-test:
PASS / FAIL




## Final Metrics

| Metric | Result |
|---|---|
| Task Success Rate | 85% |
| Tool Selection Accuracy | 100% |
| Tool Argument Accuracy | 100% |
| Answer Accuracy | 85% |
| Security Accuracy | 100% |
| Memory Accuracy | 100% |
| Retry Recovery | PASS |
| Fallback Test | PASS |
| Cache Hit Rate | 80% |
| Full State Tokens | 549 |
| Model Context Tokens | 627 |