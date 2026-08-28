from dataclasses import dataclass


@dataclass
class PermissionResult:
    allowed: bool
    reason: str
    risk_level: str


# =====================================
# Tool风险分级
# =====================================

TOOL_RISK_LEVELS = {

    "search_product": "LOW",

    "search_policy": "LOW",

    "query_order": "MEDIUM",

    "query_logistics": "MEDIUM",

    "transfer_to_human": "ACTION",
}


# =====================================
# 明确的转人工意图
# =====================================

HUMAN_SERVICE_KEYWORDS = [

    "转人工",
    "人工客服",
    "找人工",
    "联系人工",
    "我要人工",
    "人工处理",
]


def has_explicit_human_intent(
    user_text: str
) -> bool:

    return any(
        keyword in user_text
        for keyword
        in HUMAN_SERVICE_KEYWORDS
    )


def check_tool_permission(
    tool_name: str,
    user_text: str,
) -> PermissionResult:

    risk_level = (
        TOOL_RISK_LEVELS.get(
            tool_name,
            "UNKNOWN"
        )
    )


    # ==================================
    # 查询型Tool
    # ==================================

    if risk_level in {
        "LOW",
        "MEDIUM",
    }:

        return PermissionResult(
            allowed=True,
            reason="查询型Tool允许执行。",
            risk_level=risk_level,
        )


    # ==================================
    # Action Tool
    # ==================================

    if tool_name == "transfer_to_human":

        if has_explicit_human_intent(
            user_text
        ):

            return PermissionResult(
                allowed=True,
                reason=(
                    "用户明确表达了"
                    "转人工意图。"
                ),
                risk_level="ACTION",
            )

        return PermissionResult(
            allowed=False,
            reason=(
                "用户没有明确要求转人工，"
                "因此阻止Action Tool执行。"
            ),
            risk_level="ACTION",
        )


    # ==================================
    # 未知Tool默认拒绝
    # ==================================

    return PermissionResult(
        allowed=False,
        reason=(
            f"未知Tool：{tool_name}，"
            "默认拒绝执行。"
        ),
        risk_level="UNKNOWN",
    )