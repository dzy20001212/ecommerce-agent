from app.services.chat_service import (
    chat,
)


def run_test(
    question,
    expected_route,
):

    result = chat(
        question
    )


    actual_route = (
        result["route"]
    )


    passed = (
        actual_route
        == expected_route
    )


    print(
        "\nQuestion:",
        question
    )

    print(
        "Expected:",
        expected_route
    )

    print(
        "Actual:",
        actual_route
    )

    print(
        "PASS:",
        passed
    )


    return passed


if __name__ == "__main__":

    results = []


    results.append(
        run_test(
            "AirSound Pro多少钱？",
            "product",
        )
    )


    results.append(
        run_test(
            "查询订单10001",
            "order",
        )
    )


    results.append(
        run_test(
            "商品可以退货吗？",
            "service",
        )
    )


    print(
        "\nAll PASS:",
        all(results)
    )