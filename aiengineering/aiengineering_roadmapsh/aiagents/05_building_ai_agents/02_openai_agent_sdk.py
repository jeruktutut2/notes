"""
05_building_ai_agents/02_openai_agent_sdk.py
Implementasi OpenAI AgentKit & Agents SDK Patterns (Swarm & Handoff Architecture).
"""

from typing import List, Dict, Any, Tuple
from rich.console import Console
from rich.panel import Panel

console = Console()

class OpenAIAgent:
    """Representasi objek Agent pada OpenAI Agents SDK / Swarm Framework."""
    def __init__(self, name: str, instructions: str, functions: List[Any] = None):
        self.name = name
        self.instructions = instructions
        self.functions = functions or []

class HandoffResponse:
    """Objek pembungkus transfer tugas ke agen baru."""
    def __init__(self, target_agent: OpenAIAgent, message: str):
        self.target_agent = target_agent
        self.message = message

# Definisi Agen Spesialis
refund_agent = OpenAIAgent(
    name="Refund Agent",
    instructions="Anda adalah agen khusus yang menangani proses pengembalian uang (refund)."
)

triage_agent = OpenAIAgent(
    name="Triage Agent",
    instructions="Anda adalah agen garda depan. Analisis permintaan user dan transfer ke agen spesialis."
)

def transfer_to_refund_agent() -> HandoffResponse:
    """Fungsi Handoff untuk mengalihkan percakapan ke Refund Agent."""
    return HandoffResponse(refund_agent, "Mentransfer percakapan ke Refund Agent...")

triage_agent.functions.append(transfer_to_refund_agent)

class OpenAIAgentsSDKRunner:
    """Simulasi Engine Eksekusi OpenAI Agents SDK / Swarm."""

    def run_swarm_handoff_demo(self, user_prompt: str):
        console.print(Panel(f"[bold green]OpenAI Agents SDK / Swarm Pattern[/bold green]\nUser Prompt: '{user_prompt}'", title="OpenAI AgentKit Demo"))

        active_agent = triage_agent
        console.print(f"🤖 [Active Agent Initialized]: [bold yellow]{active_agent.name}[/bold yellow]")
        console.print(f"📋 Instructions: {active_agent.instructions}")

        # Step 1: Triage Agent Menganalisis
        console.print(f"\n[cyan]Step 1:[/cyan] {active_agent.name} memproses prompt user...")
        console.print(f"⚡ {active_agent.name} memutuskan memanggil tool: 'transfer_to_refund_agent()'")

        # Step 2: Eksekusi Handoff
        handoff = transfer_to_refund_agent()
        active_agent = handoff.target_agent
        console.print(f"\n🔄 [HANDOFF EVENT]: {handoff.message}")
        console.print(f"🤖 [New Active Agent]: [bold green]{active_agent.name}[/bold green]")
        console.print(f"📋 Instructions: {active_agent.instructions}")

        # Step 3: Refund Agent Menyelesaikan Tugas
        console.print(f"\n[cyan]Step 2:[/cyan] {active_agent.name} mengeksekusi aksi refund...")
        console.print("[bold green]Final Response:[/bold green] Saldo pengembalian dana telah dikirimkan ke akun Anda.")

def main():
    runner = OpenAIAgentsSDKRunner()
    runner.run_swarm_handoff_demo("Saya minta pengembalian dana untuk transaksi kemarin.")

if __name__ == "__main__":
    main()
