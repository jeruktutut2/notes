"""
04_multi_agents/multi_agent_orchestrator.py
Implementasi Topologi Multi-Agent System (Orchestrator-Worker, Sequential Chain, Router Agent).
"""

import time
from typing import Dict, Any, List
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

console = Console()

class SpecializedAgent:
    """Agent Spesialis dengan peran spesifik."""
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt

    def process(self, input_data: str) -> str:
        console.print(f"  🤖 [{self.name} - {self.role}] sedang memproses data...")
        time.sleep(0.2)
        if self.role == "Researcher":
            return f"Data Hasil Riset: 'Tren AI Agents tahun 2026 didominasi oleh Multi-Agent Systems dan On-Device Micro-Agents.'"
        elif self.role == "Writer":
            return f"Draft Artikel: Berdasarkan riset: '{input_data}', berikut ringkasan eksekutif untuk manajemen..."
        elif self.role == "Reviewer":
            return f"Hasil Review: Draft disetujui. Skor Kualitas: 9.5/10. Siap dipublikasikan."
        elif self.role == "Tech Support":
            return f"Solusi Teknis: Coba lakukan restart daemon service dengan 'systemctl restart agent-service'."
        elif self.role == "Billing Agent":
            return f"Solusi Billing: Tagihan #INV-402 telah lunas pada 2026-07-20."
        return f"Processed by {self.name}: {input_data}"


class MultiAgentOrchestrator:
    """Manager Agent yang mengatur alur kerja Multi-Agent (Orchestrator Pattern)."""
    def __init__(self):
        self.researcher = SpecializedAgent("Agent-Alpha", "Researcher", "Riset data mendalam")
        self.writer = SpecializedAgent("Agent-Beta", "Writer", "Tulis draf publikasi")
        self.reviewer = SpecializedAgent("Agent-Gamma", "Reviewer", "Review dan QA")

    def run_hierarchical_workflow(self, user_goal: str):
        console.print(Panel(f"[bold cyan]TOPOLOGI 1: HIERARCHICAL (Orchestrator-Worker)[/bold cyan]\nGoal: {user_goal}", title="Multi-Agent Execution"))
        
        console.print("👑 [Orchestrator] Memecah tugas menjadi 3 sub-task & menugaskan Agent-Alpha (Researcher)...")
        research_res = self.researcher.process(user_goal)
        console.print(f"   └── Result Alpha: {research_res}")

        console.print("👑 [Orchestrator] Mengirim hasil riset ke Agent-Beta (Writer)...")
        draft_res = self.writer.process(research_res)
        console.print(f"   └── Result Beta: {draft_res}")

        console.print("👑 [Orchestrator] Mengirim draft ke Agent-Gamma (Reviewer)...")
        final_res = self.reviewer.process(draft_res)
        console.print(f"   └── Result Gamma: {final_res}")

        console.print(f"\n[bold green]✅ Workflow Selesai![/bold green] Output Akhir:\n{final_res}\n")

    def run_router_workflow(self, user_query: str, query_type: str):
        console.print(Panel(f"[bold magenta]TOPOLOGI 2: ROUTER / DISPATCHER AGENT[/bold magenta]\nQuery: '{user_query}'", title="Multi-Agent Router"))
        
        console.print("🚦 [Router Agent] Menganalisis niat query user...")
        time.sleep(0.2)

        if query_type == "billing":
            console.print("   └── Niat terdeteksi: BILLING. Mengarahkan ke Billing Agent...")
            agent = SpecializedAgent("Agent-Finance", "Billing Agent", "Urus transaksi")
            res = agent.process(user_query)
        else:
            console.print("   └── Niat terdeteksi: TEKNIS. Mengarahkan ke Tech Support Agent...")
            agent = SpecializedAgent("Agent-DevOps", "Tech Support", "Bantu masalah server")
            res = agent.process(user_query)

        console.print(f"[bold green]Response Agent Spesialis:[/bold green] {res}\n")

def main():
    orchestrator = MultiAgentOrchestrator()
    
    # 1. Test Hierarchical Workflow
    orchestrator.run_hierarchical_workflow("Buatkan laporan tren teknologi AI Agents 2026")

    # 2. Test Router Agent Workflow
    orchestrator.run_router_workflow("Server aplikasi saya bermasalah tidak bisa konek", "tech")
    orchestrator.run_router_workflow("Status pembayaran invoice #INV-402", "billing")

if __name__ == "__main__":
    main()
