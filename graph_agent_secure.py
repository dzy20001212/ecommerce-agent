import os
import operator

from typing import Annotated, Literal
from typing_extensions import TypedDict

from dotenv import load_dotenv

from langchain_deepseek import ChatDeepSeek
from langchain.messages import (
    AnyMessage,
    HumanMessage,
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
from utils.context_manager import (
    count_message_tokens,
    trim_context,
    messages_to_text,
)

from utils.reliability import (
    execute_tool_reliably,
    get_tool_fallback,
)

from security.permissions import (
    check_tool_permission,
)


load_dotenv()


model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0,

    timeout=30,
    max_retries=2,
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

MAX_MODEL_CONTEXT_TOKENS = 800

SUMMARY_TRIGGER_TOKENS = 1000

KEEP_RECENT_MESSAGES = 8


class AgentState(
    TypedDict,
    total=False
):

    messages: Annotated[
        list[AnyMessage],
        operator.add
    ]

    llm_calls: int

    summary: str

    summarized_count: int

    summary_calls: int

    full_state_tokens: int

    model_context_tokens: int

    tool_retries: int

    tool_failures: int

    fallback_count: int

    last_error: str

    permission_denied: int

    security_events: int


    

def update_summary_if_needed(
    state: AgentState
):

    messages = state.get(
        "messages",
        []
    )

    full_tokens = (
        count_message_tokens(
            messages
        )
    )

    old_summary = state.get(
        "summary",
        ""
    )

    old_count = state.get(
        "summarized_count",
        0
    )


    # Token还没有达到阈值
    if (
        full_tokens
        < SUMMARY_TRIGGER_TOKENS
    ):
        return (
            old_summary,
            old_count,
            0,
        )


    # 最近几条消息保留原文
    cutoff = max(
        0,
        len(messages)
        - KEEP_RECENT_MESSAGES
    )


    # 没有新的老消息需要摘要
    if cutoff <= old_count:
        return (
            old_summary,
            old_count,
            0,
        )


    new_old_messages = (
        messages[
            old_count:cutoff
        ]
    )


    history_text = (
        messages_to_text(
            new_old_messages
        )
    )


    summary_prompt = f"""
你正在维护一个电商客服会话摘要。

已有摘要：
{old_summary if old_summary else "无"}

新增历史：
{history_text}

请更新摘要。

必须优先保留：
1. 用户明确提供的订单号；
2. 已查询到的商品名称；
3. 订单状态和物流结果；
4. 用户关注的售后政策；
5. 尚未解决的问题；
6. Tool返回的关键事实。

不要编造任何不存在的信息。
摘要尽量简洁。
"""


    summary_response = (
        model.invoke(
            [
                HumanMessage(
                    content=summary_prompt
                )
            ]
        )
    )


    return (
        summary_response.content,
        cutoff,
        1,
    )

def llm_call(
    state: AgentState
):

    messages = state.get(
        "messages",
        []
    )


    # ① 完整State Token
    full_state_tokens = (
        count_message_tokens(
            messages
        )
    )


    # ② 必要时更新摘要
    (
        summary,
        summarized_count,
        new_summary_calls,
    ) = update_summary_if_needed(
        state
    )


    # ③ 已经被摘要的旧消息
    # 不再重复作为原文发送给LLM
    if summarized_count > 0:

        recent_source = (
            messages[
                summarized_count:
            ]
        )

    else:

        recent_source = messages


    # ④ 裁剪最近消息
    recent_messages = trim_context(
        recent_source,
        max_tokens=(
            MAX_MODEL_CONTEXT_TOKENS
        ),
    )


    # ⑤ 最终给模型的 Context
    model_messages = [
        SystemMessage(
            content=SYSTEM_PROMPT
        )
    ]


    if summary:

        model_messages.append(
            SystemMessage(
                content=(
                    "以下是此前会话的"
                    "压缩摘要，请结合它理解"
                    "当前用户的问题：\n"
                    f"{summary}"
                )
            )
        )


    model_messages.extend(
        recent_messages
    )


    # ⑥ 统计真正发送给模型的Token
    model_context_tokens = (
        count_message_tokens(
            model_messages
        )
    )


    # ⑦ 正常Tool Calling
    response = (
        model_with_tools.invoke(
            model_messages
        )
    )


    return {
        "messages": [
            response
        ],

        "llm_calls": (
            state.get(
                "llm_calls",
                0
            )
            + 1
        ),

        "summary": summary,

        "summarized_count": (
            summarized_count
        ),

        "summary_calls": (
            state.get(
                "summary_calls",
                0
            )
            + new_summary_calls
        ),

        "full_state_tokens": (
            full_state_tokens
        ),

        "model_context_tokens": (
            model_context_tokens
        ),
    }

def get_last_user_text(
    messages
) -> str:

    for message in reversed(
        messages
    ):

        message_type = getattr(
            message,
            "type",
            ""
        )

        if message_type == "human":

            return str(
                getattr(
                    message,
                    "content",
                    ""
                )
            )

    return ""


def tool_node(
    state: AgentState
):

    results = []

    retry_count = 0
    failure_count = 0
    fallback_count = 0

    # Day 4
    permission_denied_count = 0
    security_event_count = 0

    last_error = ""


    last_message = (
        state["messages"][-1]
    )


    # 获取最近一次用户输入
    user_text = get_last_user_text(
        state["messages"]
    )


    for tool_call in (
        last_message.tool_calls
    ):

        # =========================
        # 1. 获取Tool信息
        # =========================

        tool_name = (
            tool_call["name"]
        )

        tool_args = (
            tool_call["args"]
        )


        print(
            f"\n[Tool Node] "
            f"Tool={tool_name}"
        )

        print(
            f"[Tool Node] "
            f"Args={tool_args}"
        )


        # =========================
        # 2. 找到真正的Tool对象
        # =========================

        selected_tool = (
            tools_by_name[
                tool_name
            ]
        )


        # =========================
        # 3. Day 4：
        # Permission Check
        # 第18步就加在这里
        # =========================

        permission = (
            check_tool_permission(
                tool_name,
                user_text,
            )
        )


        print(
            f"[Permission] "
            f"tool={tool_name}, "
            f"risk={permission.risk_level}, "
            f"allowed={permission.allowed}"
        )


        # =========================
        # 4. 没有权限
        # → 不执行Tool
        # =========================

        if not permission.allowed:

            print(
                f"[Permission Denied] "
                f"{permission.reason}"
            )


            results.append(
                ToolMessage(
                    content=(
                        "该操作未通过安全权限检查："
                        + permission.reason
                    ),

                    tool_call_id=(
                        tool_call["id"]
                    ),
                )
            )


            permission_denied_count += 1

            security_event_count += 1


            # 非常重要
            # 直接处理下一个Tool Call
            # 不执行下面的Tool
            continue


        # =========================
        # 5. 权限通过以后
        # 才进入Day 3 Reliability
        # =========================

        execution = (
            execute_tool_reliably(
                selected_tool,
                tool_args,
            )
        )


        retry_count += (
            execution.retries
        )


        # =========================
        # 6. Tool成功
        # =========================

        if execution.success:

            observation = (
                execution.value
            )


        # =========================
        # 7. Tool最终失败
        # → Fallback
        # =========================

        else:

            failure_count += 1

            fallback_count += 1


            if execution.error:

                last_error = (
                    f"{type(execution.error).__name__}: "
                    f"{execution.error}"
                )


            observation = (
                get_tool_fallback(
                    tool_name
                )
            )


        # =========================
        # 8. Tool结果返回给LLM
        # =========================

        results.append(
            ToolMessage(
                content=str(
                    observation
                ),

                tool_call_id=(
                    tool_call["id"]
                ),
            )
        )


    # =============================
    # 9. 更新State
    # =============================

    return {

        "messages":
            results,

        "tool_retries":
            state.get(
                "tool_retries",
                0
            )
            + retry_count,

        "tool_failures":
            state.get(
                "tool_failures",
                0
            )
            + failure_count,

        "fallback_count":
            state.get(
                "fallback_count",
                0
            )
            + fallback_count,

        "last_error":
            last_error,

        # Day 4

        "permission_denied":
            state.get(
                "permission_denied",
                0
            )
            + permission_denied_count,

        "security_events":
            state.get(
                "security_events",
                0
            )
            + security_event_count,
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