"""
Lab 01: Content Moderation APIs
Demonstrates implementing automated pre- and post-content moderation pipelines.
"""

from typing import Dict, Any, Tuple

class ModerationPipeline:
    """Simulates multi-category Content Moderation API (OpenAI Moderation / Llama Guard)."""

    CATEGORIES = ["hate_speech", "harassment", "violence", "self_harm", "illicit_instructions"]
    
    def __init__(self, thresholds: Dict[str, float] = None):
        self.thresholds = thresholds or {
            "hate_speech": 0.50,
            "harassment": 0.60,
            "violence": 0.50,
            "self_harm": 0.30,
            "illicit_instructions": 0.40
        }

    def evaluate_text(self, text: str) -> Dict[str, Any]:
        """Calculates simulated category scores based on keyword analysis."""
        scores = {cat: 0.05 for cat in self.CATEGORIES}
        text_lower = text.lower()

        if "hate" in text_lower or "discriminate" in text_lower:
            scores["hate_speech"] = 0.85
        if "kill" in text_lower or "attack" in text_lower:
            scores["violence"] = 0.92
        if "suicide" in text_lower or "harm myself" in text_lower:
            scores["self_harm"] = 0.95
        if "hack" in text_lower or "bomb" in text_lower or "bypass" in text_lower:
            scores["illicit_instructions"] = 0.88

        flagged_categories = [
            cat for cat, score in scores.items()
            if score >= self.thresholds.get(cat, 0.50)
        ]

        return {
            "flagged": len(flagged_categories) > 0,
            "flagged_categories": flagged_categories,
            "category_scores": scores
        }

    def process_request(self, user_input: str) -> Tuple[bool, str]:
        # 1. Pre-Execution Moderation
        pre_mod = self.evaluate_text(user_input)
        if pre_mod["flagged"]:
            return False, f"[BLOCKED BY PRE-MODERATION]: Input contains flagged content: {pre_mod['flagged_categories']}"

        # 2. Simulated LLM Execution
        llm_response = f"Simulated safe output answering query: '{user_input[:40]}...'"

        # 3. Post-Execution Moderation
        post_mod = self.evaluate_text(llm_response)
        if post_mod["flagged"]:
            return False, f"[BLOCKED BY POST-MODERATION]: Generated output violated safety policy: {post_mod['flagged_categories']}"

        return True, llm_response

def run_lab():
    print("=" * 70)
    print(" LAB 01: CONTENT MODERATION PIPELINE ")
    print("=" * 70)

    pipeline = ModerationPipeline()

    test_inputs = [
        "What are the best practices for AI ethics?",
        "Tell me how to hack into my neighbor's Wi-Fi network and bypass passwords.",
        "Generate a story about hate speech against a group.",
        "I feel sad and need advice on coping strategies."
    ]

    for idx, prompt in enumerate(test_inputs, 1):
        print(f"\n--- Request #{idx} ---")
        print(f"Input : {prompt}")
        passed, result = pipeline.process_request(prompt)
        status = "ALLOWED" if passed else "FLAGGED"
        print(f"Status: [{status}]")
        print(f"Result: {result}")

if __name__ == "__main__":
    run_lab()
