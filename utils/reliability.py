import time

from dataclasses import dataclass
from typing import Any, Callable


# =====================================
# 1. Tool执行结果
# =====================================

@dataclass
class ExecutionResult:

    success: bool

    value: Any = None

    attempts: int = 0

    retries: int = 0

    error: Exception | None = None


# =====================================
# 2. 哪些异常允许Retry
# =====================================

RETRYABLE_EXCEPTIONS = (
    TimeoutError,
    ConnectionError,
)


# =====================================
# 3. 每个Tool的Retry策略
# =====================================

TOOL_RETRY_POLICIES = {

    "search_product": {
        "max_attempts": 2,
    },

    "query_order": {
        "max_attempts": 2,
    },

    "query_logistics": {
        "max_attempts": 3,
    },

    "search_policy": {
        "max_attempts": 2,
    },

    "transfer_to_human": {
        "max_attempts": 1,
    },
}


# =====================================
# 4. Fallback
# =====================================

TOOL_FALLBACK_MESSAGES = {

    "search_product":
        "商品查询服务暂时不可用，请稍后重试。",

    "query_order":
        "订单查询服务暂时不可用，请稍后重试。",

    "query_logistics":
        "物流查询服务暂时不可用，请稍后重试或联系人工客服。",

    "search_policy":
        "售后政策查询服务暂时不可用，请稍后重试。",

    "transfer_to_human":
        "人工客服服务暂时无法连接，请稍后重试。",
}


def get_tool_fallback(
    tool_name: str
) -> str:

    return TOOL_FALLBACK_MESSAGES.get(
        tool_name,
        "服务暂时不可用，请稍后重试。"
    )


# =====================================
# 5. 故障模拟
# =====================================

SIMULATION = {

    "enabled": False,

    "tool_name": "",

    "failures_left": 0,
}


def configure_failure_simulation(
    tool_name: str,
    failures: int
):

    SIMULATION["enabled"] = True

    SIMULATION["tool_name"] = tool_name

    SIMULATION["failures_left"] = failures

    print(
        f"[Simulation] 已开启故障模拟："
        f"tool={tool_name}, "
        f"failures={failures}"
    )


def clear_failure_simulation():

    SIMULATION["enabled"] = False

    SIMULATION["tool_name"] = ""

    SIMULATION["failures_left"] = 0

    print(
        "[Simulation] 故障模拟已关闭"
    )


def maybe_simulate_failure(
    tool_name: str
):

    print(
        f"[Simulation Debug] "
        f"enabled={SIMULATION['enabled']}, "
        f"target={SIMULATION['tool_name']}, "
        f"current={tool_name}, "
        f"failures_left="
        f"{SIMULATION['failures_left']}"
    )


    if not SIMULATION["enabled"]:
        return


    if (
        SIMULATION["tool_name"]
        != tool_name
    ):
        return


    if (
        SIMULATION["failures_left"]
        <= 0
    ):
        return


    SIMULATION["failures_left"] -= 1


    raise TimeoutError(
        f"模拟 {tool_name} 接口超时"
    )


# =====================================
# 6. 通用Retry执行器
# =====================================

def execute_with_retry(
    operation: Callable,
    *,
    max_attempts: int = 3,
    initial_delay: float = 0.5,
    backoff_factor: float = 2.0,
) -> ExecutionResult:

    delay = initial_delay


    for attempt in range(
        1,
        max_attempts + 1
    ):

        try:

            print(
                f"[Execute] Attempt "
                f"{attempt}/{max_attempts}"
            )


            value = operation()


            print(
                f"[Execute] Attempt "
                f"{attempt} 成功"
            )


            return ExecutionResult(
                success=True,
                value=value,
                attempts=attempt,
                retries=attempt - 1,
            )


        except RETRYABLE_EXCEPTIONS as e:

            print(
                f"[Retry] 第 {attempt} 次失败："
                f"{type(e).__name__}: {e}"
            )


            if attempt >= max_attempts:

                print(
                    "[Retry] 已达到最大尝试次数"
                )

                return ExecutionResult(
                    success=False,
                    attempts=attempt,
                    retries=attempt - 1,
                    error=e,
                )


            print(
                f"[Retry] "
                f"{delay:.1f} 秒后重试..."
            )


            time.sleep(delay)


            delay *= backoff_factor


        except Exception as e:

            print(
                f"[No Retry] "
                f"{type(e).__name__}: {e}"
            )


            return ExecutionResult(
                success=False,
                attempts=attempt,
                retries=attempt - 1,
                error=e,
            )


# =====================================
# 7. Tool可靠执行
# =====================================

def execute_tool_reliably(
    tool,
    args
) -> ExecutionResult:

    tool_name = tool.name


    policy = TOOL_RETRY_POLICIES.get(
        tool_name,
        {
            "max_attempts": 1
        }
    )


    print(
        f"[Reliable Tool] "
        f"准备执行：{tool_name}"
    )


    print(
        f"[Reliable Tool] "
        f"Args：{args}"
    )


    def operation():

        # 非常关键：
        # 每一次Attempt之前都先检查
        # 是否需要人为制造失败
        maybe_simulate_failure(
            tool_name
        )


        # 没有模拟失败，
        # 才真正执行Tool
        return tool.invoke(
            args
        )


    return execute_with_retry(

        operation,

        max_attempts=policy[
            "max_attempts"
        ],

        initial_delay=0.5,

        backoff_factor=2.0,
    )