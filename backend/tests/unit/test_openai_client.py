from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from common.openai_client import OpenAIClient


def test_validation_payload_uses_safe_defaults(monkeypatch):
    client = OpenAIClient(model="test-model")
    payload = {"summary": "ok", "recommendedProducts": [], "missingInformation": ["Needs documentation"], "disclaimer": "Preliminary educational guidance only."}
    validated = client._validate_analysis_payload(payload)
    assert validated["summary"] == "ok"
    assert validated["missingInformation"] == ["Needs documentation"]
