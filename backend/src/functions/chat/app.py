import json
import os
from typing import Any, Dict

from aws_lambda_powertools import Logger, Metrics, Tracer

from common.auth import require_auth
from common.dynamodb import ProductRepository
from common.errors import AppError, ValidationError
from common.models import DEFAULT_DISCLAIMER, sanitize_product_summary
from common.openai_client import OpenAIClient
from common.response import build_error_response, build_success_response

logger = Logger(service="chat")
tracer = Tracer(service="chat")
metrics = Metrics(namespace="MortgageProductCopilot")


@tracer.capture_lambda_handler
@metrics.log_metrics
def handler(event, context):
    request_id = event.get("requestContext", {}).get("requestId") or "local"
    try:
        identity = require_auth(event)
        body = _parse_body(event)
        question = body.get("message") or body.get("question")
        if not question:
            raise ValidationError("A question is required")
        repository = ProductRepository()
        products = repository.list_products(limit=6)["items"]
        context_items = [sanitize_product_summary(product) for product in products]
        openai_client = OpenAIClient()
        answer = openai_client.generate_scenario_analysis(context_items, {"borrowerScenario": question})
        response_payload = {
            "answer": answer.get("summary", "No answer available."),
            "disclaimer": answer.get("disclaimer", DEFAULT_DISCLAIMER),
            "productsUsed": [item.get("productName") for item in context_items[:3]],
        }
        return _json_response(build_success_response(response_payload, request_id))
    except AppError as exc:
        return _json_response(build_error_response(exc.code, exc.message, request_id, exc.details), status_code=exc.status_code)
    except Exception as exc:
        logger.exception("Unhandled exception")
        return _json_response(build_error_response("INTERNAL_ERROR", "Internal server error", request_id), status_code=500)


def _parse_body(event: Dict[str, Any]) -> Dict[str, Any]:
    body = event.get("body") or "{}"
    if isinstance(body, str):
        return json.loads(body)
    return body


def _json_response(body: Dict[str, Any], status_code: int = 200) -> Dict[str, Any]:
    return {"statusCode": status_code, "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": os.getenv("ALLOWED_ORIGINS", "*")}, "body": json.dumps(body)}
