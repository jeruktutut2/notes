#!/usr/bin/env python3
"""
Modul 04: Evaluation, Testing, Debugging & Monitoring - Part 1
Simulasi Evaluasi dan Pengujian AI Agent:
- Metrik Evaluasi (Tool Accuracy, Task Completion Rate, Faithfulness, Step Efficiency)
- Unit Testing for Individual Tools
- Integration Testing for Agent Flows
- Human-in-the-Loop (HITL) Evaluation & Approval Gate
- Overview Framework Evaluasi (LangSmith, DeepEval, Ragas)
"""

import json
from typing import Dict, Any, List

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


# ============================================================================
# 1. AGENT EVALUATION METRICS CALCULATOR
# ============================================================================
class AgentEvaluator:
    """Kalkulator Metrik Kinerja dan Kualitas Agent."""

    @staticmethod
    def calculate_metrics(test_results: List[Dict[str, Any]]) -> Dict[str, float]:
        total_runs = len(test_results)
        successful_tasks = sum(1 for r in test_results if r["task_completed"])
        correct_tool_calls = sum(1 for r in test_results if r["tool_calls_correct"])
        total_tool_calls = sum(r["total_tool_calls"] for r in test_results)
        
        avg_steps = sum(r["steps_taken"] for r in test_results) / total_runs
        avg_faithfulness = sum(r.get("faithfulness_score", 1.0) for r in test_results) / total_runs

        task_completion_rate = (successful_tasks / total_runs) * 100
        tool_call_accuracy = (correct_tool_calls / total_tool_calls * 100) if total_tool_calls > 0 else 100.0

        return {
            "task_completion_rate": task_completion_rate,
            "tool_call_accuracy": tool_call_accuracy,
            "average_steps_taken": avg_steps,
            "average_faithfulness": avg_faithfulness
        }


# ============================================================================
# 2. UNIT TESTING FOR INDIVIDUAL TOOLS
# ============================================================================
def run_unit_tests_for_tools():
    print(f"\n{BOLD}{CYAN}=== 1. UNIT TESTING FOR INDIVIDUAL TOOLS ==={RESET}")
    
    def weather_tool(city: str) -> str:
        if not city:
            raise ValueError("City parameter required.")
        return f"Cuaca di {city}: 28°C, Cerah."

    # Test Cases
    test_cases = [
        {"input": "Jakarta", "expected_success": True},
        {"input": "", "expected_success": False}
    ]

    for i, tc in enumerate(test_cases, 1):
        try:
            res = weather_tool(tc["input"])
            print(f"  Test #{i} (Input: '{tc['input']}'): {GREEN}PASSED{RESET} -> {res}")
        except Exception as e:
            if not tc["expected_success"]:
                print(f"  Test #{i} (Expected Error for empty input): {GREEN}PASSED{RESET} -> Caught error: {e}")
            else:
                print(f"  Test #{i}: {RED}FAILED{RESET} -> {e}")


# ============================================================================
# 3. INTEGRATION TESTING FOR AGENT FLOWS
# ============================================================================
def run_integration_testing_flows():
    print(f"\n{BOLD}{YELLOW}=== 2. INTEGRATION TESTING FOR AGENT FLOWS ==={RESET}")
    print("Menguji trajectory alur agent secara bertahap dari prompt input hingga jawaban akhir...")

    trajectory = [
        {"step": 1, "action": "search_db", "status": "OK"},
        {"step": 2, "action": "summarize_text", "status": "OK"},
        {"step": 3, "action": "send_notification", "status": "OK"}
    ]

    all_passed = all(step["status"] == "OK" for step in trajectory)
    if all_passed:
        print(f"  {GREEN}✓ End-to-End Integration Flow Test PASSED (3/3 steps successfully executed).{RESET}")


# ============================================================================
# 4. HUMAN-IN-THE-LOOP (HITL) EVALUATION
# ============================================================================
def run_human_in_the_loop_simulation():
    print(f"\n{BOLD}{MAGENTA}=== 3. HUMAN-IN-THE-LOOP (HITL) EVALUATION ==={RESET}")
    print("Agent mendeteksi aksi sensitif/berisiko tinggi yang membutuhkan konfirmasi manusia.")

    sensitive_action = {
        "action": "delete_database_table",
        "target": "users_backup_2025",
        "risk_level": "HIGH"
    }

    print(f"  {RED}[APPROVAL GATE TRIGGERED]{RESET} Action: {sensitive_action['action']} on '{sensitive_action['target']}'")
    print(f"  {YELLOW}Mengarahkan request ke Human Evaluator Dashboard...{RESET}")
    
    # Simulasi persetujuan manusia
    human_approval = True  # Simulated approve/reject
    if human_approval:
        print(f"  {GREEN}✓ Action APPROVED by Human Supervisor (User ID: admin_01). Executing action...{RESET}")
    else:
        print(f"  {RED}✖ Action REJECTED by Human Supervisor. Cancelling action execution.{RESET}")


# ============================================================================
# DEMO EXECUTION
# ============================================================================
def main():
    print(f"{BOLD}{GREEN}===================================================={RESET}")
    print(f"{BOLD}{GREEN} MODUL 04.1: EVALUATION & TESTING FOR AI AGENTS      {RESET}")
    print(f"{BOLD}{GREEN}===================================================={RESET}")

    # 1. Metrics Calculation
    test_runs = [
        {"task_completed": True, "tool_calls_correct": 2, "total_tool_calls": 2, "steps_taken": 3, "faithfulness_score": 0.95},
        {"task_completed": True, "tool_calls_correct": 3, "total_tool_calls": 3, "steps_taken": 4, "faithfulness_score": 0.98},
        {"task_completed": False, "tool_calls_correct": 1, "total_tool_calls": 2, "steps_taken": 5, "faithfulness_score": 0.70},
    ]

    metrics = AgentEvaluator.calculate_metrics(test_runs)
    print(f"{BOLD}--- Hasil Evaluasi Metrik Runs ({len(test_runs)} test samples) ---{RESET}")
    print(f"  • Task Completion Rate: {GREEN}{metrics['task_completion_rate']:.1f}%{RESET}")
    print(f"  • Tool Call Accuracy  : {GREEN}{metrics['tool_call_accuracy']:.1f}%{RESET}")
    print(f"  • Average Steps Taken : {BLUE}{metrics['average_steps_taken']:.2f} steps{RESET}")
    print(f"  • Average Faithfulness: {BLUE}{metrics['average_faithfulness']:.2f}{RESET}")

    # 2. Tool Unit Testing
    run_unit_tests_for_tools()

    # 3. Integration Testing
    run_integration_testing_flows()

    # 4. Human-in-the-Loop
    run_human_in_the_loop_simulation()

    # 5. Evaluation Frameworks Summary
    print(f"\n{BOLD}{CYAN}=== 5. EVALUATION FRAMEWORKS OVERVIEW ==={RESET}")
    print("  • LangSmith : Datasets, Run Assertions, & Automated Prompt Testing.")
    print("  • DeepEval  : Unit Testing Pytest-style untuk G-Eval, Hallucination, & Summarization.")
    print("  • Ragas     : Framework Evaluasi RAG (Faithfulness, Context Precision/Recall).")


if __name__ == "__main__":
    main()
