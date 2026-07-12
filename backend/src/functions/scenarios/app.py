import json
import os
from typing import Any, Dict, List

from aws_lambda_powertools import Logger, Metrics, Tracer

from common.auth import require_auth
from common.dynamodb import ProductRepository
from common.errors import AppError, ValidationError
from common.models import DEFAULT_DISCLAIMER, sanitize_product_summary, sanitize_scenario
from common.openai_client import OpenAIClient
from common.response import build_error_response, build_success_response

logger = Logger(service="scenarios")
tracer = Tracer(service="scenarios")
metrics = Metrics(namespace="MortgageProductCopilot")


@tracer.capture_lambda_handler
@metrics.log_metrics
def handler(event, context):
    request_id = event.get("requestContext", {}).get("requestId") or "local"
    try:
        require_auth(event)
        body = _parse_body(event)
        scenario = body.get("scenario") or {}
        if not scenario.get("borrowerScenario"):
            raise ValidationError("Borrower scenario is required")
        repository = ProductRepository()
        products = repository.list_products(limit=20)["items"]
        relevant = [_prepare_product_context(product) for product in products]
        scored = [
            {
                **product,
                "matchScore": score_product_against_scenario(product, scenario),
            }
            for product in products
        ]
        ranked = sorted(scored, key=lambda item: item["matchScore"], reverse=True)[:5]
        openai_client = OpenAIClient()
        ai_response = openai_client.generate_scenario_analysis(relevant, sanitize_scenario(scenario))
        result = {
            "summary": ai_response.get("summary", "No summary provided."),
            "recommendedProducts": [
                {
                    "productId": item.get("id"),
                    "productName": item.get("name"),
                    "matchScore": item["matchScore"],
                    "whyItMayFit": [f"Matched relevance {item['matchScore']}/100"],
                    "concerns": ["Verify current lender guidelines."],
                    "followUpQuestions": ["What documentation does the borrower have?"],
                    "verificationNeeded": ["Confirm current lender overlays and state availability."],
                }
                for item in ranked
            ],
            "missingInformation": ai_response.get("missingInformation", []),
            "disclaimer": ai_response.get("disclaimer", DEFAULT_DISCLAIMER),
        }
        repository.save_scenario(require_auth(event)["sub"], body.get("scenarioId", "local"), {"scenario": scenario, "result": result})
        return _json_response(build_success_response(result, request_id))
    except AppError as exc:
        return _json_response(build_error_response(exc.code, exc.message, request_id, exc.details), status_code=exc.status_code)
    except Exception as exc:
        logger.exception("Unhandled exception")
        return _json_response(build_error_response("INTERNAL_ERROR", "Internal server error", request_id), status_code=500)


def score_product_against_scenario(product: Dict[str, Any], scenario: Dict[str, Any]) -> int:
    score = 0
    scenario_text = " ".join([scenario.get("borrowerScenario", ""), scenario.get("state", ""), scenario.get("propertyType", ""), scenario.get("transactionType", ""), scenario.get("employmentType", ""), scenario.get("incomeDocumentation", "")]).lower()
    product_text = " ".join([product.get("name", ""), product.get("category", ""), product.get("whatItIs", ""), product.get("bestFor", ""), product.get("problemSolved", "")]).lower()
    for term in ["self-employed", "bank statement", "p&l", "foreign", "asset", "purchase", "refinance", "investment"]:
        if term in scenario_text and term in product_text:
            score += 15
    if scenario.get("transactionType") and scenario.get("transactionType") in product.get("transactionTypes", []):
        score += 25
    if scenario.get("occupancy") and scenario.get("occupancy") in product.get("occupancy", []):
        score += 20
    if scenario.get("propertyType") and scenario.get("propertyType") in product.get("propertyTypes", []):
        score += 20
    return min(score, 100)


def _prepare_product_context(product: Dict[str, Any]) -> Dict[str, Any]:
    return sanitize_product_summary(product)


def _parse_body(event: Dict[str, Any]) -> Dict[str, Any]:
    body = event.get("body") or "{}"
    if isinstance(body, str):
        return json.loads(body)
    return body


def _json_response(body: Dict[str, Any], status_code: int = 200) -> Dict[str, Any]:
    return {"statusCode": status_code, "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": os.getenv("ALLOWED_ORIGINS", "*")}, "body": json.dumps(body)}
