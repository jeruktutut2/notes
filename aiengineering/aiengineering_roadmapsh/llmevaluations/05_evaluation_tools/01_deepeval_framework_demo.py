"""
01_deepeval_framework_demo.py
-----------------------------
Demonstrasi Framework DeepEval (Confident AI):
1. Penggunaan DeepEval LLMTestCase & Metrics
2. Simulasi GEval, AnswerRelevancy, & Hallucination Metrics
3. Penjelasan Struktur PyTest Integration untuk CI/CD
"""

import sys

# Simulation wrapper for DeepEval test cases when deepeval SDK is not installed or running offline
class DeepEvalSimulatedSuite:
    def __init__(self):
        self.test_cases = []

    def add_test_case(self, input_text: str, actual_output: str, expected_output: str = None, context: list[str] = None):
        self.test_cases.append({
            "input": input_text,
            "actual_output": actual_output,
            "expected_output": expected_output,
            "context": context or []
        })

    def run_evaluations(self) -> list[dict]:
        results = []
        for idx, tc in enumerate(self.test_cases, 1):
            # Simulated metric evaluations
            geval_score = 0.92
            relevancy_score = 0.95
            hallucination_score = 0.05 # low score = clean from hallucination
            passed = geval_score >= 0.7 and relevancy_score >= 0.7 and hallucination_score <= 0.3

            results.append({
                "test_id": f"DEEPEVAL-TEST-{idx}",
                "input": tc["input"],
                "actual_output": tc["actual_output"],
                "metrics": {
                    "GEval (CoT)": {"score": geval_score, "threshold": 0.7, "passed": geval_score >= 0.7},
                    "AnswerRelevancy": {"score": relevancy_score, "threshold": 0.7, "passed": relevancy_score >= 0.7},
                    "Hallucination": {"score": hallucination_score, "threshold": 0.3, "passed": hallucination_score <= 0.3}
                },
                "overall_passed": passed
            })
        return results

if __name__ == "__main__":
    print("=== LAB 12: DEEPEVAL FRAMEWORK SIMULATION & METRICS ===")

    suite = DeepEvalSimulatedSuite()

    suite.add_test_case(
        input_text="Apa fungsi utama dari DeepEval?",
        actual_output="DeepEval adalah framework unit testing open-source untuk LLM yang memfasilitasi pengujian berulang dan CI/CD.",
        expected_output="DeepEval digunakan untuk pengujian LLM otomatis berbasis PyTest.",
        context=["DeepEval memfasilitasi LLM unit testing dengan built-in metrics seperti GEval, Hallucination, dan AnswerRelevancy."]
    )

    eval_results = suite.run_evaluations()

    for res in eval_results:
        print(f"\n[Test Case ID]: {res['test_id']}")
        print(f" Input         : '{res['input']}'")
        print(f" Actual Output : '{res['actual_output']}'")
        print(f" Test Status   : {'✅ PASSED (Ready for CI/CD)' if res['overall_passed'] else '❌ FAILED'}")
        print(" Detailed Metrics:")
        for m_name, m_val in res['metrics'].items():
            status_icon = "✓" if m_val['passed'] else "✗"
            print(f"   - {m_name:<18}: Score {m_val['score']:.2f} (Threshold: {m_val['threshold']}) [{status_icon}]")

    print("\n💡 PyTest Integration Note:")
    print("   Untuk menjalankan dalam CI/CD dengan DeepEval SDK asli, gunakan CLI:")
    print("   $ deepeval test run 05_evaluation_tools/01_deepeval_framework_demo.py")
