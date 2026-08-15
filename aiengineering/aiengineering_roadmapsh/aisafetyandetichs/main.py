"""
AI Safety and Ethics - Master CLI Suite
Run any of the interactive hands-on safety & ethics labs.
"""

import os
import sys
import subprocess

LABS = {
    "1": ("Prompt Injection Attacks & Defenses", "01_understanding_safety_issues/01_prompt_injection.py"),
    "2": ("Security & Privacy (PII Masking & Output Checks)", "01_understanding_safety_issues/02_security_privacy.py"),
    "3": ("Bias & Fairness Audit", "01_understanding_safety_issues/03_bias_fairness.py"),
    "4": ("Content Moderation Pipeline", "02_safety_best_practices/01_content_moderation.py"),
    "5": ("End-User ID Tracking & Rate Limiting", "02_safety_best_practices/02_user_id_tracking.py"),
    "6": ("Adversarial Testing (Red Teaming)", "02_safety_best_practices/03_adversarial_testing.py"),
    "7": ("Robust Prompt Engineering", "02_safety_best_practices/04_robust_prompt_engineering.py"),
    "8": ("KYC & Use-Case Domain Boundaries", "02_safety_best_practices/05_kyc_and_usecase_boundaries.py"),
    "9": ("Constraining Inputs & Pydantic Outputs", "02_safety_best_practices/06_constraining_inputs_outputs.py")
}

def display_menu():
    print("\n" + "=" * 70)
    print("      AI SAFETY AND ETHICS LEARNING WORKSPACE - CLI LAB RUNNER")
    print("=" * 70)
    print("\n[Module 01: Understanding AI Safety Issues]")
    print("  1. Prompt Injection Attacks & Defenses")
    print("  2. Security & Privacy (PII Masking & Output Security Checks)")
    print("  3. Bias & Fairness Audit (Disparate Impact & Counterfactuals)")
    print("\n[Module 02: Safety Best Practices]")
    print("  4. Content Moderation Pipeline")
    print("  5. End-User ID Tracking & Rate Limiting")
    print("  6. Adversarial Testing (Red Teaming)")
    print("  7. Robust Prompt Engineering (XML Tagging & Defenses)")
    print("  8. KYC & Use-Case Domain Boundaries (HITL Triggers)")
    print("  9. Constraining Inputs & Outputs (Pydantic Validation)")
    print("\n  A. Run ALL Labs Sequentially")
    print("  Q. Quit")
    print("=" * 70)

def run_script(rel_path: str):
    abs_path = os.path.join(os.path.dirname(__file__), rel_path)
    print(f"\nExecuting: {rel_path}...\n")
    subprocess.run([sys.executable, abs_path])

def main():
    while True:
        display_menu()
        choice = input("\nSelect lab number to execute (1-9, A, Q): ").strip().upper()
        
        if choice == 'Q':
            print("\nExiting AI Safety and Ethics CLI. Happy learning!")
            break
        elif choice == 'A':
            for num in sorted(LABS.keys(), key=int):
                title, rel_path = LABS[num]
                print(f"\n>>> Running Lab #{num}: {title} <<<")
                run_script(rel_path)
            input("\nPress Enter to return to main menu...")
        elif choice in LABS:
            title, rel_path = LABS[choice]
            run_script(rel_path)
            input("\nPress Enter to return to main menu...")
        else:
            print("\nInvalid choice. Please enter a valid number (1-9), 'A', or 'Q'.")

if __name__ == "__main__":
    main()
