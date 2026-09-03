import json
import uuid

from datetime import datetime
from pathlib import Path


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parents[1]
)


LOG_DIR = (
    BASE_DIR
    / "logs"
)


LOG_DIR.mkdir(
    exist_ok=True
)


LOG_FILE = (
    LOG_DIR
    / "week7_observability.jsonl"
)


def new_request_id() -> str:

    return (
        "req_"
        + uuid.uuid4().hex[:10]
    )


def log_event(
    request_id: str,
    event: str,
    **fields
):

    record = {
        "timestamp":
            datetime.now().isoformat(
                timespec="milliseconds"
            ),

        "request_id":
            request_id,

        "event":
            event,

        **fields,
    }


    with open(
        LOG_FILE,
        "a",
        encoding="utf-8",
    ) as f:

        f.write(
            json.dumps(
                record,
                ensure_ascii=False,
            )
            + "\n"
        )