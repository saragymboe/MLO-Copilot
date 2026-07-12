import json
import os
import sys
from pathlib import Path

import boto3

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "mortgage_product_finder_data.json"


def main() -> None:
    table_name = os.getenv("DYNAMODB_TABLE_NAME", "MortgageProductCopilot-dev")
    region = os.getenv("AWS_REGION", "us-east-1")
    client = boto3.resource("dynamodb", region_name=region)
    table = client.Table(table_name)
    with DATA_FILE.open("r", encoding="utf-8") as handle:
        products = json.load(handle)
    for product in products:
        product_id = product["id"]
        item = dict(product)
        item["PK"] = f"PRODUCT#{product_id}"
        item["SK"] = "METADATA"
        item["GSI1PK"] = f"CATEGORY#{product.get('category', 'unknown')}"
        item["GSI1SK"] = f"PRODUCT#{product['name']}"
        item["entityType"] = "Product"
        table.put_item(Item=item)
    print(f"Seeded {len(products)} products into {table_name}")


if __name__ == "__main__":
    main()
