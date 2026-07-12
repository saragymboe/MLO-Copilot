import json
import os
from typing import Any, Dict

from aws_lambda_powertools import Logger, Metrics, Tracer

from common.auth import require_auth
from common.dynamodb import ProductRepository
from common.errors import AppError, NotFoundError
from common.response import build_error_response, build_success_response

logger = Logger(service="conversations")
tracer = Tracer(service="conversations")
metrics = Metrics(namespace="MortgageProductCopilot")


@tracer.capture_lambda_handler
@metrics.log_metrics
def handler(event, context):
    request_id = event.get("requestContext", {}).get("requestId") or "local"
    try:
        identity = require_auth(event)
        path = event.get("rawPath") or event.get("path") or ""
        method = event.get("requestContext", {}).get("http", {}).get("method") or event.get("httpMethod")
        repository = ProductRepository()
        if path == "/conversations" and method == "GET":
            items = repository.list_conversations(identity["sub"])
            return _json_response(build_success_response({"items": items}, request_id))
        if path.startswith("/conversations/") and method == "GET":
            conversation_id = path.split("/", 2)[2]
            item = repository.get_conversation(identity["sub"], conversation_id)
            if not item:
                raise NotFoundError("Conversation not found")
            return _json_response(build_success_response(item, request_id))
        if path.startswith("/conversations/") and method == "DELETE":
            conversation_id = path.split("/", 2)[2]
            repository.delete_conversation(identity["sub"], conversation_id)
            return _json_response(build_success_response({"deleted": True}, request_id), status_code=204)
        raise NotFoundError("Route not found")
    except AppError as exc:
        return _json_response(build_error_response(exc.code, exc.message, request_id, exc.details), status_code=exc.status_code)
    except Exception as exc:
        logger.exception("Unhandled exception")
        return _json_response(build_error_response("INTERNAL_ERROR", "Internal server error", request_id), status_code=500)


def _json_response(body: Dict[str, Any], status_code: int = 200) -> Dict[str, Any]:
    return {"statusCode": status_code, "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": os.getenv("ALLOWED_ORIGINS", "*")}, "body": json.dumps(body)}
