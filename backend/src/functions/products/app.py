import json
import os
import sys
from typing import Any, Dict, Optional

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.utilities.validation import Validator

from common.auth import AuthError, is_admin, require_auth
from common.dynamodb import ProductRepository
from common.errors import AppError, NotFoundError, UnauthorizedError, ValidationError
from common.response import build_error_response, build_success_response

logger = Logger(service="products")
tracer = Tracer(service="products")
metrics = Metrics(namespace="MortgageProductCopilot")


@tracer.capture_lambda_handler
@metrics.log_metrics
def handler(event, context):
    request_id = event.get("requestContext", {}).get("requestId") or "local"
    try:
        path = event.get("rawPath") or event.get("path") or ""
        method = event.get("requestContext", {}).get("http", {}).get("method") or event.get("httpMethod")
        if path == "/products" and method == "GET":
            return _list_products(event, request_id)
        if path.startswith("/products/") and method == "GET":
            product_id = path.split("/", 2)[2]
            return _get_product(product_id, event, request_id)
        if path == "/admin/products" and method == "POST":
            return _create_product(event, request_id)
        if path.startswith("/admin/products/") and method == "PUT":
            product_id = path.split("/", 3)[3]
            return _update_product(product_id, event, request_id)
        if path.startswith("/admin/products/") and method == "DELETE":
            product_id = path.split("/", 3)[3]
            return _delete_product(product_id, event, request_id)
        if path == "/admin/products/import" and method == "POST":
            return _import_products(event, request_id)
        raise NotFoundError("Route not found")
    except AppError as exc:
        logger.exception("Request failed")
        return _json_response(build_error_response(exc.code, exc.message, request_id, exc.details), status_code=exc.status_code)
    except Exception as exc:
        logger.exception("Unhandled exception")
        return _json_response(build_error_response("INTERNAL_ERROR", "Internal server error", request_id), status_code=500)


def _list_products(event, request_id: str):
    repository = ProductRepository()
    params = event.get("queryStringParameters") or {}
    result = repository.list_products(category=params.get("category"), lender=params.get("lender"), limit=int(params.get("limit", 20)))
    return _json_response(build_success_response({"items": result["items"], "nextToken": result.get("nextToken")}, request_id))


def _get_product(product_id: str, event, request_id: str):
    repository = ProductRepository()
    item = repository.get_product(product_id)
    if not item:
        raise NotFoundError("Product not found")
    return _json_response(build_success_response(item, request_id))


def _create_product(event, request_id: str):
    require_auth(event)
    if not is_admin(event):
        raise UnauthorizedError("Admin authorization required")
    body = _parse_body(event)
    if not body.get("name"):
        raise ValidationError("Product name is required")
    repository = ProductRepository()
    product = repository.put_product(body)
    return _json_response(build_success_response(product, request_id), status_code=201)


def _update_product(product_id: str, event, request_id: str):
    require_auth(event)
    if not is_admin(event):
        raise UnauthorizedError("Admin authorization required")
    body = _parse_body(event)
    repository = ProductRepository()
    product = repository.update_product(product_id, body)
    return _json_response(build_success_response(product, request_id))


def _delete_product(product_id: str, event, request_id: str):
    require_auth(event)
    if not is_admin(event):
        raise UnauthorizedError("Admin authorization required")
    repository = ProductRepository()
    repository.delete_product(product_id)
    return _json_response(build_success_response({"deleted": True}, request_id), status_code=204)


def _import_products(event, request_id):
    require_auth(event)
    if not is_admin(event):
        raise UnauthorizedError("Admin authorization required")
    body = _parse_body(event)
    items = body.get("products") or []
    repository = ProductRepository()
    for product in items:
        repository.put_product(product)
    return _json_response(build_success_response({"imported": len(items)}), request_id)


def _parse_body(event: Dict[str, Any]) -> Dict[str, Any]:
    body = event.get("body") or "{}"
    if isinstance(body, str):
        return json.loads(body)
    return body


def _json_response(body: Dict[str, Any], status_code: int = 200) -> Dict[str, Any]:
    return {"statusCode": status_code, "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": os.getenv("ALLOWED_ORIGINS", "*")}, "body": json.dumps(body)}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", dest="seed_file")
    args = parser.parse_args()
    if args.seed_file:
        import json
        from pathlib import Path
        with open(args.seed_file, "r", encoding="utf-8") as handle:
            products = json.load(handle)
        repository = ProductRepository()
        for product in products:
            repository.put_product(product)
