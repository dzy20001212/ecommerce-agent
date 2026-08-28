from statistics import mean

from services.cached_agent import (
    ask_stateless_with_cache,
)

from cache.redis_cache import (
    redis_client,
)

from redis.exceptions import RedisError

try:
    redis_client.flushdb()
    print("Redis 缓存已清空")

except RedisError as e:
    print(f"Redis 当前不可用，跳过清空缓存：{e}")


question = (
    "AirSound Pro支持主动降噪吗？"
)


# redis_client.flushdb()


results = []


for i in range(5):

    result = (
        ask_stateless_with_cache(
            question
        )
    )

    results.append(result)

    print(
        f"Run {i + 1}: "
        f"hit={result['cache_hit']}, "
        f"time={result['elapsed_ms']:.2f}ms, "
        f"llm_calls={result['llm_calls']}"
    )


times = [
    r["elapsed_ms"]
    for r in results
]


print("\n===== Benchmark =====")

print(
    "第一次请求：",
    f"{times[0]:.2f} ms"
)

print(
    "后续平均缓存响应：",
    f"{mean(times[1:]):.2f} ms"
)

print(
    "总 LLM Calls：",
    sum(
        r["llm_calls"]
        for r in results
    )
)

print(
    "Cache Hit Count：",
    sum(
        1
        for r in results
        if r["cache_hit"]
    )
)


hit_count = sum(
    1
    for r in results
    if r["cache_hit"]
)

hit_rate = (
    hit_count
    / len(results)
)


print(
    "Cache Hit Rate:",
    f"{hit_rate:.2%}"
)