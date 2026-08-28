import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def load_json(file_name: str):
    file_path = DATA_DIR / file_name

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


PRODUCTS = load_json("products.json")
ORDERS = load_json("orders.json")
LOGISTICS = load_json("logistics.json")
POLICIES = load_json("policies.json")