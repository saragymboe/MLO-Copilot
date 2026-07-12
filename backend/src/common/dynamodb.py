import os
from typing import Any, Dict, List, Optional

import boto3

from common.config import CONFIG


class ProductRepository:
    def __init__(self, table_name: Optional[str] = None) -> None:
        self.table_name = table_name or CONFIG.table_name
        self.client = boto3.resource("dynamodb", region_name=CONFIG.region)
        self.table = self.client.Table(self.table_name)

    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        response = self.table.get_item(Key={"PK": f"PRODUCT#{product_id}", "SK": "METADATA"})
        item = response.get("Item")
        return item if item else None

    def list_products(self, *, category: Optional[str] = None, lender: Optional[str] = None, limit: int = 20, pagination_token: Optional[str] = None) -> Dict[str, Any]:
        if category:
            response = self.table.query(
                IndexName="GSI1",
                KeyConditionExpression="GSI1PK = :pk",
                ExpressionAttributeValues={":pk": f"CATEGORY#{category}"},
                Limit=limit,
            )
        else:
            response = self.table.scan(Limit=limit)
        items = response.get("Items", [])
        return {"items": items, "nextToken": response.get("LastEvaluatedKey")}

    def put_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        product_id = product["id"]
        product["PK"] = f"PRODUCT#{product_id}"
        product["SK"] = "METADATA"
        product["GSI1PK"] = f"CATEGORY#{product.get('category', 'unknown')}"
        product["GSI1SK"] = f"PRODUCT#{product['name']}"
        product["entityType"] = "Product"
        self.table.put_item(Item=product)
        return product

    def update_product(self, product_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        existing = self.get_product(product_id) or {}
        merged = {**existing, **updates}
        merged["PK"] = f"PRODUCT#{product_id}"
        merged["SK"] = "METADATA"
        merged["GSI1PK"] = f"CATEGORY#{merged.get('category', 'unknown')}"
        merged["GSI1SK"] = f"PRODUCT#{merged['name']}"
        merged["entityType"] = "Product"
        self.table.put_item(Item=merged)
        return merged

    def delete_product(self, product_id: str) -> None:
        self.table.delete_item(Key={"PK": f"PRODUCT#{product_id}", "SK": "METADATA"})

    def save_conversation(self, user_sub: str, conversation_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        item = {"PK": f"USER#{user_sub}", "SK": f"CONVERSATION#{conversation_id}", "entityType": "Conversation", **payload}
        self.table.put_item(Item=item)
        return item

    def list_conversations(self, user_sub: str) -> List[Dict[str, Any]]:
        response = self.table.query(
            KeyConditionExpression="PK = :pk and begins_with(SK, :prefix)",
            ExpressionAttributeValues={":pk": f"USER#{user_sub}", ":prefix": "CONVERSATION#"},
        )
        return response.get("Items", [])

    def get_conversation(self, user_sub: str, conversation_id: str) -> Optional[Dict[str, Any]]:
        response = self.table.get_item(Key={"PK": f"USER#{user_sub}", "SK": f"CONVERSATION#{conversation_id}"})
        return response.get("Item")

    def delete_conversation(self, user_sub: str, conversation_id: str) -> None:
        self.table.delete_item(Key={"PK": f"USER#{user_sub}", "SK": f"CONVERSATION#{conversation_id}"})

    def save_message(self, conversation_id: str, message: Dict[str, Any]) -> Dict[str, Any]:
        item = {"PK": f"CONVERSATION#{conversation_id}", "SK": f"MESSAGE#{message['timestamp']}#{message['id']}", "entityType": "Message", **message}
        self.table.put_item(Item=item)
        return item

    def save_scenario(self, user_sub: str, scenario_id: str, scenario: Dict[str, Any]) -> Dict[str, Any]:
        item = {"PK": f"USER#{user_sub}", "SK": f"SCENARIO#{scenario_id}", "entityType": "Scenario", **scenario}
        self.table.put_item(Item=item)
        return item

    def get_user_profile(self, user_sub: str) -> Optional[Dict[str, Any]]:
        response = self.table.get_item(Key={"PK": f"USER#{user_sub}", "SK": "PROFILE"})
        return response.get("Item")

    def put_user_profile(self, user_sub: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        item = {"PK": f"USER#{user_sub}", "SK": "PROFILE", "entityType": "UserProfile", **profile}
        self.table.put_item(Item=item)
        return item
