# Week 5 Day 1 - Agent 基础与 Tool Calling

## 1. 今日目标

- 理解 LLM、RAG 和 Agent 的区别
- 理解 Tool 的基本概念
- 理解 Tool Calling 的完整执行流程
- 使用 LangChain 定义 Tool
- 构建一个简单的电商客服 Agent
- 验证 Agent 是否能够自主选择 Tool




## 2. 核心知识

### 2.1 LLM

普通 LLM 的基本流程：

User
→ Prompt
→ LLM
→ Answer

LLM 主要负责自然语言理解、推理和生成。


### 2.2 RAG

RAG 的基本流程：

User
→ Retrieval
→ Relevant Documents
→ LLM
→ Answer

RAG 主要解决模型缺少外部知识的问题。


### 2.3 Agent

Agent 在 LLM 基础上增加了决策和工具调用能力。

基本流程：

User
→ LLM
→ Tool Call
→ Tool
→ Tool Result
→ LLM
→ Answer

Agent 可以根据用户问题自主决定是否调用工具，以及调用哪个工具。





## 3. Tool

Tool 可以理解为提供给 Agent 使用的具体能力。

本项目目前实现三个 Tool：

1. search_product
   - 查询商品信息

2. query_order
   - 查询订单信息

3. search_policy
   - 查询退款、退货、换货政策

Tool 可以理解为：

Tool = Function + Name + Description + Parameter Schema



LLM 本身不会直接执行 Python 函数。

LLM 首先生成 Tool Call：

Tool Name + Arguments

随后 LangChain 执行真正的 Python Tool，
再把 Tool Result 返回给 LLM。


## 4. 当前 Tools

### search_product

输入：

product_name: str

示例：

AirSound Pro

返回：

{
    "price": 799,
    "noise_cancelling": true,
    "color": "black"
}


### query_order

输入：

order_id: str

示例：

10001

返回：

{
    "product": "AirSound Pro",
    "status": "已发货"
}


### search_policy

输入：

topic: str

示例：

退款

返回：

商品未发货时可以申请退款。







## 5. Tool 独立测试

运行命令：

python test_tools.py

测试结果：

### Test 1

Tool:

search_product

Input:

AirSound Pro

Result:

{'price': 799, 'noise_cancelling': True, 'color': 'black'}

Status:

PASS


### Test 2

Tool:

query_order

Input:

10001

Result:

{'product': 'AirSound Pro', 'status': '已发货'}

Status:

PASS


### Test 3

Tool:

search_policy

Input:

退款

Result:

商品未发货时可以申请退款。

Status:

PASS


## 6. Agent Tool Calling 测试

### Case 1：订单查询

Question:

订单10001发货了吗？

Expected Tool:

query_order

Actual Tool:

query_order

Result:

PASS




### Case 2：商品查询

Question:

AirSound Pro 支持主动降噪吗？

Expected Tool:

search_product

Actual Tool:

search_product

Result:

PASS



### Case 3：售后政策

Question:

商品没发货可以退款吗？

Expected Tool:

search_policy

Actual Tool:

search_policy

Result:

PASS



### Case 4：普通对话

Question:

你好，你是谁？

Expected Tool:

None

Actual Tool:

None

Result:

PASS



## 7. Multi-step Tool Calling

Question:

订单10001里的商品支持主动降噪吗？

Expected:

query_order
→ search_product
→ final answer

Actual:

query_order
→ search_product
→ final answer

Result:

PASS




## 8. Summary

今天完成了 Agent 基础知识学习，并搭建了 ecommerce-agent 项目。

主要完成：

- 创建 Python 虚拟环境
- 安装 LangChain
- 实现 search_product、query_order、search_policy 三个 Tool
- 完成三个 Tool 的独立测试
- 理解 Tool Calling 基本执行流程
- 开始搭建基于 LLM 的 Agent

下一步：

继续完成 Agent Tool Calling 测试，并优化 Tool Description。