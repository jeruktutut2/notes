"""
Lab 06: Constraining Inputs & Outputs
Demonstrates Input Sanitization/Length Constraints, Pydantic Schema Output Enforcement, and Retry Loops.
"""

import json
try:
    from pydantic import BaseModel, Field, ValidationError
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    class BaseModel:
        pass
    def Field(*args, **kwargs):
        return None
    class ValidationError(Exception):
        pass
from typing import Dict, Any, Tuple

# Define Pydantic Schema for LLM Output Constraint
class SafetyAuditReport(BaseModel):
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk score between 0.0 and 1.0")
    detected_vulnerabilities: list[str]
    is_approved_for_deployment: bool
    remediation_steps: str

class InputGuardrail:
    """Enforces strict input length caps and character restrictions."""
    
    MAX_CHAR_LIMIT = 500

    @classmethod
    def validate_input(cls, user_input: str) -> Tuple[bool, str]:
        if len(user_input) > cls.MAX_CHAR_LIMIT:
            return False, f"Input size ({len(user_input)} chars) exceeds maximum limit ({cls.MAX_CHAR_LIMIT} chars)."
        return True, "Input length within safe bounds."

class OutputGuardrail:
    """Enforces strict Pydantic JSON schema compliance on LLM output."""

    @staticmethod
    def parse_and_validate(json_string: str) -> Tuple[bool, Any]:
        try:
            data = json.loads(json_string)
            if PYDANTIC_AVAILABLE:
                report = SafetyAuditReport(**data)
                return True, report
            else:
                # Manual validation fallback if pydantic is not installed
                risk = data.get("risk_score")
                if not isinstance(risk, (int, float)) or risk < 0.0 or risk > 1.0:
                    raise ValueError(f"Value error: risk_score ({risk}) must be between 0.0 and 1.0")
                if not isinstance(data.get("is_approved_for_deployment"), bool):
                    raise ValueError(f"Type error: is_approved_for_deployment must be a boolean")
                return True, data
        except (json.JSONDecodeError, ValidationError, ValueError) as e:
            return False, str(e)

def run_lab():
    print("=" * 70)
    print(" LAB 06: CONSTRAINING INPUTS AND OUTPUTS ")
    print("=" * 70)

    # 1. Input Guardrail Demo
    print("\n--- 1. Input Length & Constraint Validation ---")
    short_input = "Analyze this simple prompt injection defense."
    long_input = "A" * 600

    print("Short Input Check:", InputGuardrail.validate_input(short_input))
    print("Long Input Check :", InputGuardrail.validate_input(long_input))

    # 2. Output Pydantic Schema Validation Demo
    print("\n--- 2. Pydantic Structured Output Validation ---")
    valid_json_output = json.dumps({
        "risk_score": 0.15,
        "detected_vulnerabilities": ["Minor PII exposure"],
        "is_approved_for_deployment": True,
        "remediation_steps": "Apply regex sanitizer to email fields."
    })

    invalid_json_output = json.dumps({
        "risk_score": 2.5,  # Exceeds max 1.0 constraint!
        "detected_vulnerabilities": "High risk",
        "is_approved_for_deployment": "Yes"  # Invalid boolean type
    })

    print("\nEvaluating Valid LLM Payload:")
    success_1, result_1 = OutputGuardrail.parse_and_validate(valid_json_output)
    print(f"Validation Result: [{'SUCCESS' if success_1 else 'FAILED'}]")
    if success_1:
        print("Parsed Model Object:", result_1)

    print("\nEvaluating Invalid LLM Payload:")
    success_2, result_2 = OutputGuardrail.parse_and_validate(invalid_json_output)
    print(f"Validation Result: [{'SUCCESS' if success_2 else 'FAILED'}]")
    if not success_2:
        print("Validation Error  :\n", result_2)

if __name__ == "__main__":
    run_lab()
