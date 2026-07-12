from typing import Any, Dict, List

DEFAULT_DISCLAIMER = "Preliminary educational guidance only. This is not a loan approval or commitment to lend. Verify current lender guidelines, overlays, pricing, state availability, property eligibility, and underwriting requirements."


def sanitize_product_summary(product: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "productId": product.get("id"),
        "productName": product.get("name"),
        "category": product.get("category"),
        "lendersVisible": product.get("lendersVisible"),
        "whatItIs": product.get("whatItIs"),
        "problemSolved": product.get("problemSolved"),
        "bestFor": product.get("bestFor"),
        "guidelines": product.get("guidelines") or ["Verify current lender guidelines."],
    }


def sanitize_scenario(scenario: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "borrowerScenario": scenario.get("borrowerScenario", ""),
        "state": scenario.get("state"),
        "transactionType": scenario.get("transactionType"),
        "occupancy": scenario.get("occupancy"),
        "propertyType": scenario.get("propertyType"),
        "employmentType": scenario.get("employmentType"),
        "incomeDocumentation": scenario.get("incomeDocumentation"),
        "creditScoreRange": scenario.get("creditScoreRange"),
        "downPaymentRange": scenario.get("downPaymentRange"),
        "citizenship": scenario.get("citizenship"),
        "priorEvents": scenario.get("priorEvents"),
        "timeSensitivity": scenario.get("timeSensitivity"),
        "notes": scenario.get("notes"),
    }
