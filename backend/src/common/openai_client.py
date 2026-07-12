import json
import os
import time
from typing import Any, Dict, Optional

import boto3
from openai import OpenAI

from common.config import CONFIG


class OpenAIClient:
    def __init__(self, model: Optional[str] = None) -> None:
        self.model = model or CONFIG.openai_model
        self.timeout = CONFIG.openai_timeout_seconds
        self._client: Optional[OpenAI] = None
        self._secret_cache: Optional[str] = None

    def _get_api_key(self) -> str:
        if self._secret_cache:
            return self._secret_cache
        if not CONFIG.openai_secret_arn:
            raise RuntimeError("OPENAI_SECRET_ARN is required")
        client = boto3.client("secretsmanager", region_name=CONFIG.region)
        response = client.get_secret_value(SecretId=CONFIG.openai_secret_arn)
        secret = response.get("SecretString") or ""
        self._secret_cache = secret
        return secret

    def _get_client(self) -> OpenAI:
        if self._client is None:
            self._client = OpenAI(api_key=self._get_api_key(), timeout=self.timeout)
        return self._client

    def generate_scenario_analysis(self, product_context: list[Dict[str, Any]], scenario: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = (
            "You are an internal mortgage product educational assistant. "
            "Use only the supplied product context for product-specific conclusions. "
            "Do not promise qualification, approval, interest rates, fees, or final terms. "
            "Clearly identify missing data and direct the user to verify current lender guidelines, pricing, overlays, state availability, and underwriting requirements."
        )
        user_payload = json.dumps({"products": product_context, "scenario": scenario}, ensure_ascii=False)
        for attempt in range(2):
            try:
                response = self._get_client().responses.create(
                    model=self.model,
                    input=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_payload},
                    ],
                    temperature=0.2,
                    max_output_tokens=900,
                    text={"format": {"type": "json_object"}},
                )
                data = json.loads(response.output_text)
                return self._validate_analysis_payload(data)
            except Exception:
                if attempt == 1:
                    return {
                        "summary": "AI guidance is temporarily unavailable.",
                        "recommendedProducts": [],
                        "missingInformation": ["Confirm product availability and lender guidance manually."],
                        "disclaimer": "Preliminary educational guidance only. This is not a loan approval or commitment to lend. Verify current lender guidelines, overlays, pricing, state availability, property eligibility, and underwriting requirements.",
                    }
                time.sleep(1)

    def _validate_analysis_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        recommended = payload.get("recommendedProducts") or []
        if not isinstance(recommended, list):
            raise ValueError("recommendedProducts must be a list")
        return {
            "summary": payload.get("summary", "No summary provided."),
            "recommendedProducts": recommended,
            "missingInformation": payload.get("missingInformation", []),
            "disclaimer": payload.get("disclaimer", "Preliminary educational guidance only. Verify current lender guidelines, overlays, pricing, state availability, property eligibility, and underwriting requirements."),
        }
