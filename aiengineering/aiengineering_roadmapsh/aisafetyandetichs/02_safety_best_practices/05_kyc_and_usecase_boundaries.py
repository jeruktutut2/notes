"""
Lab 05: Know Your Customers / Use-Cases & Domain Boundaries
Demonstrates domain boundary checking, risk tiering, and Human-in-the-Loop (HITL) escalation.
"""

from typing import Dict, Any, Tuple

class DomainBoundaryEnforcer:
    """Enforces allowed application scope and risk boundaries before executing LLM actions."""

    ALLOWED_DOMAINS = ["customer_support", "product_faq", "account_billing"]
    HIGH_RISK_KEYWORDS = ["wire_transfer", "delete_account", "medical_diagnosis", "legal_advice", "prescribe"]

    @classmethod
    def evaluate_request_scope(cls, domain: str, query: str) -> Tuple[str, str]:
        """
        Evaluates query for scope and risk.
        Returns risk level: LOW_RISK, OUT_OF_SCOPE, or HIGH_RISK_HITL_REQUIRED.
        """
        query_lower = query.lower()

        # 1. Domain Check
        if domain not in cls.ALLOWED_DOMAINS:
            return "OUT_OF_SCOPE", f"Domain '{domain}' is not authorized for this AI deployment."

        # 2. High-Risk / HITL Keyword Check
        for kw in cls.HIGH_RISK_KEYWORDS:
            if kw in query_lower or kw.replace("_", " ") in query_lower:
                return "HIGH_RISK_HITL_REQUIRED", f"Request involves sensitive action ('{kw}'). Requires explicit Human-in-the-Loop approval."

        return "LOW_RISK", "Request within authorized domain boundaries."

def run_lab():
    print("=" * 70)
    print(" LAB 05: KYC & USE-CASE DOMAIN BOUNDARIES ")
    print("=" * 70)

    test_queries = [
        ("customer_support", "How do I update my billing address in the mobile app?"),
        ("medical_portal", "What dosage of medicine should I take for severe chest pain?"),
        ("account_billing", "I want to initiate a wire transfer of $50,000 to an external bank."),
        ("customer_support", "Can you give me legal advice on breaking my office lease?")
    ]

    for domain, query in test_queries:
        print(f"\n--- Domain: {domain} ---")
        print(f"Query : {query}")
        risk_level, decision = DomainBoundaryEnforcer.evaluate_request_scope(domain, query)
        print(f"Risk Tier : [{risk_level}]")
        print(f"Action    : {decision}")

if __name__ == "__main__":
    run_lab()
