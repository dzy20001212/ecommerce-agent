from fastapi.testclient import (
    TestClient,
)

from main import app


client = TestClient(
    app
)


def test_health():

    response = client.get(
        "/health"
    )

    assert (
        response.status_code
        == 200
    )

    data = response.json()

    assert (
        data["status"]
        == "ok"
    )


def test_product_chat():

    response = client.post(
        "/chat",
        json={
            "message":
                "AirSound Pro多少钱？"
        },
    )

    assert (
        response.status_code
        == 200
    )

    data = response.json()

    assert (
        data["route"]
        == "product"
    )

    assert (
        "product"
        in data["agents"]
    )

    assert (
        "search_product"
        in data["tools"]
    )