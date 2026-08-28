import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from tools import (
    search_product,
    query_order,
    query_logistics,
    search_policy,
    transfer_to_human,
)


load_dotenv()


model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,
)


tools = [
    search_product,
    query_order,
    query_logistics,
    search_policy,
    transfer_to_human,
]


SYSTEM_PROMPT = """
你是一名电商智能客服助手。

你需要根据用户问题决定是否调用工具。

工具职责：

1. search_product
查询商品价格、颜色、参数和功能。

2. query_order
查询订单基本信息、订单状态以及是否发货。

3. query_logistics
查询具体物流运输进度、快递公司、
快递单号和最新物流节点。

4. search_policy
查询退款、退货、换货等售后政策。

5. transfer_to_human
只有用户明确要求人工客服或人工处理时才使用。

多轮对话要求：

- 可以结合当前会话的历史消息理解用户问题。
- “它”“这个订单”“这个商品”等指代，
  应根据历史上下文确定对象。
- 如果无法确定具体订单或商品，不允许猜测，
  应要求用户补充信息。

要求：

- 根据真实用户意图选择工具。
- 不要因为有工具就强制调用工具。
- 一个工具能够解决时不要调用无关工具。
- 如果完成问题需要多个工具，可以继续调用其他工具。
- 只根据工具返回的信息回答。
- 不允许编造商品、订单、物流和售后信息。
- 工具没有提供的信息要明确说明无法确认。
"""

checkpointer = InMemorySaver()
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)