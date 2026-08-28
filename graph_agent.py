import os
import operator

from typing import Annotated, Literal
from typing_extensions import TypedDict

from dotenv import load_dotenv

from langchain_deepseek import ChatDeepSeek

from langchain.messages import (
    AnyMessage,
    SystemMessage,
    ToolMessage,
)

from langgraph.graph import (
    StateGraph,
    START,
    END,
)

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


tools_by_name = {
    tool.name: tool
    for tool in tools
}


model_with_tools = model.bind_tools(tools)


SYSTEM_PROMPT = """
你是一名电商智能客服助手。

你可以使用以下工具：

1. search_product
查询商品价格、颜色、参数和功能。

2. query_order
查询订单基本信息和是否发货。

3. query_logistics
查询物流运输进度。

4. search_policy
查询退款、退货和换货政策。

5. transfer_to_human
用户明确要求人工客服时使用。

要求：

- 根据用户真实意图选择工具。
- 一个工具能够解决时不要调用无关工具。
- 如果需要多个工具，可以继续调用。
- 不允许编造工具没有返回的数据。
- 可以结合当前会话历史理解用户指代。
"""


class AgentState(TypedDict):

    messages: Annotated[
        list[AnyMessage],
        operator.add
    ]

    llm_calls: int


def llm_call(state: AgentState):

    response = model_with_tools.invoke(
        [
            SystemMessage(
                content=SYSTEM_PROMPT
            )
        ]
        + state["messages"]
    )

    return {
        "messages": [response],
        "llm_calls": state.get(
            "llm_calls",
            0
        ) + 1,
    }


def tool_node(state: AgentState):

    results = []

    last_message = state["messages"][-1]

    for tool_call in last_message.tool_calls:

        selected_tool = tools_by_name[
            tool_call["name"]
        ]

        observation = selected_tool.invoke(
            tool_call["args"]
        )

        results.append(
            ToolMessage(
                content=observation,
                tool_call_id=tool_call["id"],
            )
        )

    return {
        "messages": results
    }


def should_continue(
    state: AgentState
) -> Literal["tool_node", END]:

    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tool_node"

    return END


builder = StateGraph(AgentState)


builder.add_node(
    "llm_call",
    llm_call
)

builder.add_node(
    "tool_node",
    tool_node
)


builder.add_edge(
    START,
    "llm_call"
)


builder.add_conditional_edges(
    "llm_call",
    should_continue,
    [
        "tool_node",
        END,
    ]
)


builder.add_edge(
    "tool_node",
    "llm_call"
)


checkpointer = InMemorySaver()


graph_agent = builder.compile(
    checkpointer=checkpointer
)