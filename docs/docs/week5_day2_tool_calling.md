# Week 5 Day 2 - Tool Calling

## 1. 今日目标

- 理解 bind_tools
- 理解 Tool Schema
- 理解 Tool Call 的底层过程
- 优化 Tool Description
- 增加物流和人工客服 Tool
- 建立 Tool Selection 测试集


## 2. Tool Calling Flow

User
→ Model
→ Tool Call
→ Program
→ Tool
→ Tool Result
→ Model
→ Final Answer


## 3. bind_tools 与 Agent

bind_tools:

模型可以生成 Tool Call，
但程序需要自行执行 Tool。

create_agent:

Agent 自动完成：

Model
→ Tool
→ Result
→ Model

循环。


## 4. Current Tools

search_product

query_order

query_logistics

search_policy

transfer_to_human


## 5. Tool Selection Evaluation

测试问题数量：

12

正确数量：12

填写真实结果

Accuracy：100%

填写真实结果


## 6. Bad Cases

没有出错的问题


## 7. 今日总结

完成 Tool Calling 底层流程实验，
掌握 Tool Description 和参数 Schema
对 Agent 工具选择的影响。