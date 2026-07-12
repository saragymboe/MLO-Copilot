from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from functions.scenarios.app import score_product_against_scenario


def test_score_product_against_scenario_uses_key_terms():
    product = {"name": "Bank Statement Loan", "category": "Non-QM", "whatItIs": "A bank statement loan.", "bestFor": "Self-employed borrowers", "problemSolved": "Self-employed borrowers", "transactionTypes": ["purchase"], "occupancy": ["primary"], "propertyTypes": ["single_family"]}
    scenario = {"borrowerScenario": "Self-employed borrower with one year in business", "transactionType": "purchase", "occupancy": "primary", "propertyType": "single_family"}
    score = score_product_against_scenario(product, scenario)
    assert score >= 70
