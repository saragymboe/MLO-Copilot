import json
import os
from typing import Any, Dict

from aws_lambda_powertools import Logger, Metrics, Tracer

from common.auth import require_auth
from common.dynamodb import ProductRepository
from common.errors import AppError
from common.response import build_error_response, build_success_response

logger = Logger(service="users")
tracer = Tracer(service="users")
metrics = Metrics(namespace="MortgageProductCopilot")


@tracer.capture_lambda_handler
@metrics.log_metrics
def handler(event, context):
    request_id = event.get("requestContext", {}).get("requestId") or "local"
    try:
        identity = require_auth(event)
        repository = ProductRepository()
        profile = repository.get_user_profile(identity["sub"]) or {}
        profile.setdefault("email", identity.get("email"))
        profile.setdefault("groups", identity.get("groups", []))
        repository.put_user_profile(identity["sub"], profile)
        return _json_response(build_success_response(profile, request_id))
    except AppError as exc:
        return _json_response(build_error_response(exc.code, exc.message, request_id, exc.details), status_code=exc.status_code)
    except Exception as exc:
        logger.exception("Unhandled exception")
        return _json_response(build_error_response("INTERNAL_ERROR", "Internal server error", request_id), status_code=500)


def _json_response(body: Dict[str, Any], status_code: int = 200) -> Dict[str, Any]:
    return {"statusCode": status_code, "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": os.getenv("ALLOWED_ORIGINS", "*")}, "body": json.dumps(body)}
