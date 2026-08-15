"""
Lab 02: Security and Privacy Concerns
Demonstrates PII Masking, Data Sanitization, and Output Security Checks.
"""

import re
from typing import Dict, Tuple

class PIISanitizer:
    """Detects and redacts Personally Identifiable Information (PII) before sending context to LLMs."""
    
    PATTERNS = {
        "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "PHONE": r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b"
    }

    @classmethod
    def sanitize(cls, text: str) -> Tuple[str, Dict[str, int]]:
        sanitized_text = text
        stats = {}

        for pii_type, pattern in cls.PATTERNS.items():
            matches = re.findall(pattern, sanitized_text)
            if matches:
                stats[pii_type] = len(matches)
                sanitized_text = re.sub(pattern, f"[{pii_type}_REDACTED]", sanitized_text)

        return sanitized_text, stats

class OutputSecurityChecker:
    """Inspects LLM output for potential security vulnerabilities like XSS or dangerous code injection."""
    
    DANGEROUS_PATTERNS = [
        r"<script.*?>.*?</script>",
        r"javascript:",
        r"DROP\s+TABLE",
        r"SELECT\s+.*\s+FROM\s+information_schema"
    ]

    @classmethod
    def validate_output(cls, output: str) -> Tuple[bool, str]:
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, output, re.IGNORECASE):
                return False, f"Flagged dangerous pattern matching: {pattern}"
        return True, "Output clean"

def run_lab():
    print("=" * 70)
    print(" LAB 02: SECURITY AND PRIVACY CONCERNS ")
    print("=" * 70)

    # 1. PII Redaction Demo
    raw_user_context = (
        "User profile update: Contact John Doe at john.doe@example.com or call 555-123-4567. "
        "SSN reference: 123-45-6789. Card details: 4111-2222-3333-4444."
    )
    print("\n--- Scenario 1: PII Sanitization Before LLM Processing ---")
    print("Raw Input       :", raw_user_context)
    
    sanitized_text, stats = PIISanitizer.sanitize(raw_user_context)
    print("\nSanitized Input :", sanitized_text)
    print("Redaction Stats :", stats)

    # 2. Output Security Checks Demo
    print("\n--- Scenario 2: Insecure Output Handling Prevention ---")
    llm_outputs = [
        "Here is the code summary for your webpage.",
        "Thank you! Visit our site: <script>alert('XSS Steal Token');</script>",
        "To check the user count run: SELECT * FROM users WHERE active = 1;"
    ]

    for idx, sample_output in enumerate(llm_outputs, 1):
        is_safe, reason = OutputSecurityChecker.validate_output(sample_output)
        status = "PASSED" if is_safe else "REJECTED"
        print(f"\nSample Output {idx}: {sample_output}")
        print(f"Validation Status: [{status}] -> Reason: {reason}")

if __name__ == "__main__":
    run_lab()
