"""
main.py
CLI Interactive Runner untuk Modul Pembelajaran AI Agents (roadmap.sh AI Engineer).
"""

import sys
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

MODULES = {
    "1": ("01. AI Agents Usecases Demo", "01_agents_usecases/demo_usecases.py"),
    "2": ("02. ReAct Prompting Engine", "02_react_prompting/react_engine.py"),
    "3": ("03. Tools & Function Calling Demo", "03_tools_and_function_calling/tool_calling_demo.py"),
    "4": ("04. Multi-Agent System Orchestrator", "04_multi_agents/multi_agent_orchestrator.py"),
    "5": ("05.1 Building Agents: Manual Implementation", "05_building_ai_agents/01_manual_implementation.py"),
    "6": ("05.2 Building Agents: OpenAI AgentKit / SDK", "05_building_ai_agents/02_openai_agent_sdk.py"),
    "7": ("05.3 Building Agents: Claude Agent SDK", "05_building_ai_agents/03_claude_agent_sdk.py"),
    "8": ("05.4 Building Agents: Vertex AI Agent Builder", "05_building_ai_agents/04_vertex_ai_agent_builder.py"),
    "9": ("05.5 Building Agents: Google ADK", "05_building_ai_agents/05_google_adk.py"),
}

def display_menu():
    console.clear()
    console.print(Panel.fit(
        "[bold yellow]🤖 AI AGENTS LEARNING WORKSPACE (roadmap.sh/ai-engineer)[/bold yellow]\n"
        "[dim]Pilih modul Python yang ingin Anda jalankan secara interaktif:[/dim]",
        title="Main Menu"
    ))

    for key, (title, filepath) in MODULES.items():
        console.print(f" [bold cyan][{key}][/bold cyan] {title} [dim]({filepath})[/dim]")
    
    console.print(" [bold red][Q][/bold red] Keluar\n")

def run_script(filepath: str):
    console.print(f"\n🚀 Menjalankan [bold cyan]{filepath}[/bold cyan]...\n")
    try:
        subprocess.run([sys.executable, filepath], check=True)
    except Exception as e:
        console.print(f"[bold red]Error saat menjalankan script:[/bold red] {e}")
    
    Prompt.ask("\nTekan [Enter] untuk kembali ke menu utama")

def main():
    while True:
        display_menu()
        choice = Prompt.ask("Masukkan pilihan Anda", choices=list(MODULES.keys()) + ["q", "Q"], default="1")
        
        if choice.lower() == "q":
            console.print("[yellow]Terima kasih! Selamat belajar AI Agents.[/yellow]")
            break
        
        if choice in MODULES:
            _, filepath = MODULES[choice]
            run_script(filepath)

if __name__ == "__main__":
    main()
