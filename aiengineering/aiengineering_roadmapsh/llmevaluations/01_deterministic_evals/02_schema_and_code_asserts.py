"""
02_schema_and_code_asserts.py
-----------------------------
Demonstrasi Evaluasi Deterministik berbasis:
1. Validasi JSON & Pydantic Schema Output
2. Verifikasi Sintaks Kode Python via AST Parsing
3. Assertion Unit Testing terhadap Kode yang Dihasilkan LLM
"""

import ast
import json
from typing import List, Optional
try:
    from pydantic import BaseModel, Field, ValidationError
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    class BaseModel: pass
    def Field(*args, **kwargs): return None
    class ValidationError(Exception): pass

# 1. Pydantic Model Schema definition
class ModelEvaluationResult(BaseModel):
    model_name: str = Field(..., description="Nama model AI")
    score: float = Field(..., ge=0.0, le=1.0, description="Skor dari 0.0 sampai 1.0")
    tags: List[str] = Field(default_factory=list)
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)

def validate_json_schema(json_str: str) -> dict:
    """Validasi string JSON terhadap Pydantic schema atau fallback dict validation."""
    try:
        data = json.loads(json_str)
        if HAS_PYDANTIC:
            validated_obj = ModelEvaluationResult(**data)
            parsed_data = validated_obj.model_dump()
        else:
            # Fallback pure python manual validation
            score = data.get("score")
            if not isinstance(score, (int, float)) or not (0.0 <= score <= 1.0):
                raise ValueError("Field 'score' must be float between 0.0 and 1.0")
            if not isinstance(data.get("tags"), list):
                raise ValueError("Field 'tags' must be a list")
            parsed_data = data
            
        return {
            "valid": True,
            "parsed_data": parsed_data,
            "error": None
        }
    except json.JSONDecodeError as e:
        return {"valid": False, "parsed_data": None, "error": f"Invalid JSON Syntax: {e}"}
    except (ValidationError, ValueError) as e:
        return {"valid": False, "parsed_data": None, "error": f"Schema Validation Error: {e}"}

def check_python_syntax(code_str: str) -> dict:
    """Memeriksa apakah string kode Python valid secara sintaks menggunakan AST."""
    try:
        ast.parse(code_str)
        return {"syntax_valid": True, "error": None}
    except SyntaxError as e:
        return {
            "syntax_valid": False,
            "error": f"SyntaxError line {e.lineno}: {e.msg}"
        }

def execute_code_unit_test(generated_code: str, test_cases: List[dict]) -> dict:
    """
    Menjalankan fungsi buatan LLM dalam lingkungan eksekusi terbatas 
    dan menguji dengan assertion test cases.
    """
    local_scope = {}
    try:
        # Evaluate & compile code
        compiled_code = compile(generated_code, "<string>", "exec")
        exec(compiled_code, {}, local_scope)
    except Exception as e:
        return {"success": False, "error": f"Code Compilation/Execution Error: {e}", "passed_tests": 0, "total_tests": len(test_cases)}

    passed = 0
    test_results = []
    
    for idx, tc in enumerate(test_cases, 1):
        func_name = tc["function_name"]
        inputs = tc["inputs"]
        expected = tc["expected"]
        
        if func_name not in local_scope:
            test_results.append({"test": idx, "passed": False, "error": f"Function '{func_name}' not defined in code."})
            continue
            
        try:
            actual = local_scope[func_name](*inputs)
            if actual == expected:
                passed += 1
                test_results.append({"test": idx, "passed": True, "input": inputs, "output": actual})
            else:
                test_results.append({"test": idx, "passed": False, "input": inputs, "output": actual, "expected": expected})
        except Exception as err:
            test_results.append({"test": idx, "passed": False, "error": f"Runtime Exception: {err}"})

    return {
        "success": passed == len(test_cases),
        "passed_tests": passed,
        "total_tests": len(test_cases),
        "details": test_results
    }


if __name__ == "__main__":
    print("=== LAB 02: SCHEMA & CODE ASSERTION EVALS ===")

    # 1. Test Valid JSON Schema Output
    valid_json = '{"model_name": "GPT-4o", "score": 0.95, "tags": ["fast", "accurate"], "confidence": 0.98}'
    invalid_json = '{"model_name": "LLama-3", "score": 1.5, "tags": "invalid_array_type"}' # Score > 1.0 & wrong tag type
    
    print("\n[1] Pydantic Schema Validation:")
    print(" -> Testing Valid Output:")
    res_valid = validate_json_schema(valid_json)
    print(f"    Status: {'PASSED' if res_valid['valid'] else 'FAILED'}")
    print(f"    Parsed: {res_valid['parsed_data']}")
    
    print(" -> Testing Invalid Output (Out-of-range score & invalid types):")
    res_invalid = validate_json_schema(invalid_json)
    print(f"    Status: {'PASSED' if res_invalid['valid'] else 'FAILED (Caught Expected Error)'}")
    print(f"    Error : {res_invalid['error']}")

    # 2. Test Python AST Syntax Check
    python_code = """
def calculate_factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * calculate_factorial(n - 1)
"""
    broken_code = """
def calculate_factorial(n: int) -> int
    return n * 2
"""
    print("\n[2] AST Python Syntax Validator:")
    print(f" -> Valid Code Check : {check_python_syntax(python_code)}")
    print(f" -> Broken Code Check: {check_python_syntax(broken_code)}")

    # 3. Test Code Execution Assertion Tests
    print("\n[3] Sandboxed Code Assertion Execution:")
    code_llm = """
def is_palindrome(s: str) -> bool:
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]
"""
    unit_tests = [
        {"function_name": "is_palindrome", "inputs": ["racecar"], "expected": True},
        {"function_name": "is_palindrome", "inputs": ["A man, a plan, a canal: Panama"], "expected": True},
        {"function_name": "is_palindrome", "inputs": ["hello world"], "expected": False},
    ]
    eval_res = execute_code_unit_test(code_llm, unit_tests)
    print(f"    Passed Tests: {eval_res['passed_tests']}/{eval_res['total_tests']}")
    print(f"    Overall Success: {eval_res['success']}")
    for detail in eval_res['details']:
        print(f"    - Test {detail['test']}: {'PASS' if detail['passed'] else 'FAIL'}")
