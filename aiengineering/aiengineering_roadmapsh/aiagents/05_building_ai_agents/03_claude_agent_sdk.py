"""
05_building_ai_agents/03_claude_agent_sdk.py
Implementasi Claude Agent SDK & Anthropic Tool Use API Architecture.
"""

import json
from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel

console = Console()

class ClaudeToolUseAgent:
    """Simulasi Agentic Loop berbasis Anthropic Claude Tool Use API."""

    def __init__(self, model_name: str = "claude-3-5-sonnet-20241022"):
        self.model_name = model_name
        self.tools = [
            {
                "name": "bash_command",
                "description": "Menjalankan perintah shell bash di lingkungan terisolasi.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Command bash yang akan dijalankan"}
                    },
                    "required": ["command"]
                }
            }
        ]

    def run_agentic_loop(self, task: str):
        console.print(Panel(f"[bold magenta]Claude Agent SDK (Anthropic Tool Use API)[/bold magenta]\nModel: {self.model_name}\nTask: '{task}'", title="Claude Agent Demo"))

        # Step 1: Initial Prompt -> Claude mengembalikan tool_use block
        console.print("\n[cyan]Turn 1: User -> Claude[/cyan]")
        console.print("📩 Sending messages payload with tools definition...")

        # Simulated API Response Content Block
        simulated_claude_response = {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Saya akan mengecek ruang penyimpanan disk menggunakan command bash 'df -h'."
                },
                {
                    "type": "tool_use",
                    "id": "toolu_01A89",
                    "name": "bash_command",
                    "input": {"command": "df -h"}
                }
            ]
        }

        console.print(f"🤖 [Claude Response Block - Text]: {simulated_claude_response['content'][0]['text']}")
        tool_block = simulated_claude_response['content'][1]
        console.print(f"⚙️ [Claude Response Block - Tool Use]: name='{tool_block['name']}', input={tool_block['input']}")

        # Step 2: Client Execution
        console.print("\n[yellow]Executing Bash Command locally...[/yellow]")
        simulated_bash_output = "Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        50G   12G   38G  24% /"

        # Step 3: Feeding Tool Result Block back to Claude
        tool_result_message = {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_block["id"],
                    "content": simulated_bash_output
                }
            ]
        }
        console.print("\n[cyan]Turn 2: Tool Result -> Claude[/cyan]")
        console.print(f"📥 [Injected tool_result content block]:\n{simulated_bash_output}")

        # Step 4: Final Answer
        console.print("\n[bold green]Final Response from Claude:[/bold green]")
        console.print("Penyimpanan disk server utama masih sangat aman. Terpakai 12GB dari total 50GB (24%).")

def main():
    agent = ClaudeToolUseAgent()
    agent.run_agentic_loop("Cek ketersediaan ruang disk pada server")

if __name__ == "__main__":
    main()
