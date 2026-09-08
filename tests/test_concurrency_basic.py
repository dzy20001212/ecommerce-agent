from concurrent.futures import ThreadPoolExecutor
from time import perf_counter

import requests


URL = "http://127.0.0.1:8000/chat"


QUESTIONS = [
    "AirSound Pro多少钱？",
    "查询订单10001",
    "订单10001物流到哪里了？",
]


def send_request(question: str):
    start = perf_counter()

    response = requests.post(
        URL,
        json={
            "message": question,
        },
        timeout=60,
    )

    latency = (
        perf_counter() - start
    )

    return {
        "question": question,
        "status_code":
            response.status_code,
        "latency_seconds":
            round(latency, 2),
        "response":
            response.json(),
    }


def main():

    start = perf_counter()

    with ThreadPoolExecutor(
        max_workers=3
    ) as executor:

        results = list(
            executor.map(
                send_request,
                QUESTIONS,
            )
        )

    total = perf_counter() - start

    for result in results:
        print(
            "\nQuestion:",
            result["question"],
        )

        print(
            "Status:",
            result["status_code"],
        )

        print(
            "Latency:",
            result["latency_seconds"],
            "s",
        )

        print(
            "Route:",
            result["response"].get(
                "route"
            ),
        )

    print(
        "\nTotal Time:",
        round(total, 2),
        "s",
    )


if __name__ == "__main__":
    main()