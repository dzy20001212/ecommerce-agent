from langchain_core.messages.utils import (
    trim_messages,
    count_tokens_approximately,
)


DEFAULT_MAX_CONTEXT_TOKENS = 800


def count_message_tokens(messages) -> int:

    if not messages:
        return 0

    return count_tokens_approximately(
        messages
    )


def trim_context(
    messages,
    max_tokens: int = DEFAULT_MAX_CONTEXT_TOKENS
):
    """
    保留最近且完整的消息，
    控制发送给 LLM 的上下文长度。
    """

    if not messages:
        return []

    return trim_messages(
        messages,
        strategy="last",
        token_counter=count_tokens_approximately,
        max_tokens=max_tokens,
        start_on="human",
        end_on=("human", "tool"),
        allow_partial=False,
    )
def message_to_text(message) -> str:
    """
    将 Message 转成便于摘要模型理解的文本。
    """

    role = getattr(
        message,
        "type",
        "unknown"
    )

    content = getattr(
        message,
        "content",
        ""
    )

    text = (
        f"{role}: {content}"
    )

    tool_calls = getattr(
        message,
        "tool_calls",
        None
    )

    if tool_calls:
        text += (
            f"\nTool Calls: "
            f"{tool_calls}"
        )

    return text


def messages_to_text(messages) -> str:

    return "\n\n".join(
        message_to_text(message)
        for message in messages
    )