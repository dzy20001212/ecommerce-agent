import os
import json
import hashlib

import redis
from redis.exceptions import RedisError
from dotenv import load_dotenv


load_dotenv()


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

DEFAULT_TTL = int(
    os.getenv(
        "CACHE_TTL_SECONDS",
        "3600"
    )
)


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
)


def check_redis() -> bool:
    """
    检查 Redis 是否可用。
    """
    try:
        return bool(redis_client.ping())

    except RedisError:
        return False


def normalize_text(text: str) -> str:
    """
    对用户问题做简单标准化。
    """
    return " ".join(
        text.strip().lower().split()
    )


def build_cache_key(
    namespace: str,
    text: str
) -> str:
    """
    根据文本生成稳定的缓存 Key。
    """

    normalized = normalize_text(text)

    digest = hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()

    return (
        f"ecommerce:"
        f"{namespace}:"
        f"{digest}"
    )


def get_json(key: str):
    """
    从 Redis 获取 JSON 数据。
    Cache Miss 时返回 None。
    """

    try:
        value = redis_client.get(key)

        if value is None:
            return None

        return json.loads(value)

    except RedisError as e:
        print(
            f"[Redis Warning] "
            f"读取缓存失败：{e}"
        )

        return None


def set_json(
    key: str,
    value,
    ttl: int = DEFAULT_TTL
) -> bool:
    """
    将 JSON 数据写入 Redis，
    并设置 TTL。
    """

    try:
        redis_client.set(
            key,
            json.dumps(
                value,
                ensure_ascii=False
            ),
            ex=ttl,
        )

        return True

    except RedisError as e:
        print(
            f"[Redis Warning] "
            f"写入缓存失败：{e}"
        )

        return False


def delete_key(key: str) -> bool:
    """
    删除指定缓存。
    """

    try:
        redis_client.delete(key)
        return True

    except RedisError:
        return False


