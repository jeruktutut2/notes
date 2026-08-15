#!/usr/bin/env python3
"""
Modul 01: Common Architectures - Part 3
Simulasi Multi-Agent Systems & Self-Critique / Reflection Agents
"""

import time
from typing import List, Dict, Any

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
# 1. MULTI-AGENT SYSTEM (MANAGER - WORKER - REVIEWER PATTERN)
# ============================================================================
class Agent:
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt

    def process(self, input_message: str) -> str:
        print(f"\n[{self.name} - {self.role}] Menerima pesan...")
        if self.role == "Researcher":
            return f"Penelitian Komprehensif: Ditemukan 3 algoritma optimasi utama (AdamW, Lion, SOAP)."
        elif self.role == "Coder":
            return f"Kode Python Implementation:\n  def optimize_model(params):\n      return AdamW(params, lr=1e-4)"
        elif self.role == "Reviewer":
            return f"Review Result: PASSED. Kode sudah efisien, bebas dari bug sintaks dan type error."
        return "OK"


class MultiAgentSystem:
    """Orkestrasi sistem multi-agent menggunakan pola Hierarchical Manager."""

    def __init__(self):
        self.manager = Agent("Orchestrator", "Manager", "Membagi tugas dan memverifikasi kualitas akhir.")
        self.researcher = Agent("Researcher-01", "Researcher", "Mencari informasi teknis.")
        self.coder = Agent("Dev-01", "Coder", "Menulis sintaks kode berdasarkan riset.")
        self.reviewer = Agent("QA-01", "Reviewer", "Menganalisis kode dan memberikan verifikasi.")

    def run_collaboration(self, project_goal: str):
        print(f"\n{BOLD}{CYAN}=== MULTI-AGENT SYSTEM COLLABORATION ==={RESET}")
        print(f"Project Goal: '{project_goal}'\n")

        # Step 1: Manager to Researcher
        print(f"{YELLOW}[STEP 1]{RESET} {self.manager.name} mendagangkan tugas riset ke {self.researcher.name}...")
        research_output = self.researcher.process(project_goal)
        print(f"  └─ Hasil Riset: {BLUE}{research_output}{RESET}")

        # Step 2: Manager to Coder
        print(f"\n{YELLOW}[STEP 2]{RESET} {self.manager.name} menugaskan {self.coder.name} membuat kode berdasarkan hasil riset...")
        code_output = self.coder.process(research_output)
        print(f"  └─ Hasil Kode:\n{GREEN}{code_output}{RESET}")

        # Step 3: Manager to Reviewer
        print(f"\n{YELLOW}[STEP 3]{RESET} {self.manager.name} menugaskan {self.reviewer.name} meninjau kode...")
        review_output = self.reviewer.process(code_output)
        print(f"  └─ Verifikasi QA: {MAGENTA}{review_output}{RESET}")

        print(f"\n{BOLD}{GREEN}✓ Kolaborasi Multi-Agent Selesai Ditutup oleh Manager!{RESET}")


# ============================================================================
# 2. SELF-CRITIQUE / REFLECTION AGENT
# ============================================================================
class SelfCritiqueAgent:
    """Agent yang mengkritik dan memperbaiki outputnya sendiri secara berulang."""

    def __init__(self, quality_threshold: float = 0.90):
        self.threshold = quality_threshold

    def _generate_draft(self, topic: str, iteration: int) -> str:
        if iteration == 1:
            return "Python adalah bahasa pemrograman yang mudah dipelajari untuk AI."
        elif iteration == 2:
            return "Python adalah bahasa berorientasi objek yang sangat populer untuk AI dan Data Science karena ekosistem pustakanya (PyTorch, TensorFlow)."
        else:
            return "Python adalah bahasa berorientasi objek berpemerataan tinggi yang menjadi standar industri AI/ML. Pustaka seperti PyTorch, NumPy, dan Transformers memungkinkan eksekusi algoritma canggih secara efisien."

    def _evaluate_critic(self, draft: str) -> Dict[str, Any]:
        length = len(draft)
        contains_keywords = any(kw in draft for kw in ["PyTorch", "Transformers", "ML"])
        
        score = min(1.0, (length / 200) * 0.6 + (0.4 if contains_keywords else 0.1))
        
        feedback = []
        if length < 100:
            feedback.append("Teks terlalu singkat, tambahkan detail ekosistem.")
        if not contains_keywords:
            feedback.append("Sebutkan pustaka spesifik seperti PyTorch atau Transformers.")

        return {
            "score": score,
            "feedback": feedback if feedback else ["Kualitas jawaban sangat baik dan komprehensif."]
        }

    def run_reflection_loop(self, topic: str, max_iterations: int = 3):
        print(f"\n{BOLD}{MAGENTA}=== SELF-CRITIQUE / REFLECTION AGENT EXECUTION ==={RESET}")
        print(f"Topic: '{topic}' | Quality Target Threshold: {self.threshold * 100}%\n")

        for iter_num in range(1, max_iterations + 1):
            print(f"{BOLD}--- Iterasi Perbaikan #{iter_num} ---{RESET}")
            
            # Step 1: Draft Generation
            draft = self._generate_draft(topic, iter_num)
            print(f"  {CYAN}[GENERATOR DRAFT]:{RESET} \"{draft}\"")

            # Step 2: Critic Evaluation
            eval_result = self._evaluate_critic(draft)
            score = eval_result["score"]
            feedback = eval_result["feedback"]

            print(f"  {YELLOW}[CRITIC EVALUATION]:{RESET} Score: {score * 100:.1f}%")
            print(f"  └─ Feedback: {RED if score < self.threshold else GREEN}{' | '.join(feedback)}{RESET}")

            # Decision Gate
            if score >= self.threshold:
                print(f"\n{BOLD}{GREEN}✓ Quality Threshold Tercapai pada Iterasi #{iter_num}! Output Akhir Diterima.{RESET}\n")
                return draft
            else:
                print(f"  └─ Retrying refinement pada iterasi berikutnya...\n")

        print(f"{BOLD}{YELLOW}! Batas iterasi tercapai. Mengembalikan draft terbaik.{RESET}")


# ============================================================================
# DEMO EXECUTION
# ============================================================================
def main():
    print(f"{BOLD}{GREEN}===================================================={RESET}")
    print(f"{BOLD}{GREEN} MODUL 01.3: MULTI-AGENT & SELF-CRITIQUE AGENTS    {RESET}")
    print(f"{BOLD}{GREEN}===================================================={RESET}")

    # Demo 1: Multi-Agent Collaboration
    mas = MultiAgentSystem()
    mas.run_collaboration("Implementasi Algoritma Optimasi Deep Learning")

    # Demo 2: Self-Critique / Reflection Loop
    reflector = SelfCritiqueAgent(quality_threshold=0.85)
    reflector.run_reflection_loop("Penjelasan Keunggulan Bahasa Python dalam AI")


if __name__ == "__main__":
    main()
