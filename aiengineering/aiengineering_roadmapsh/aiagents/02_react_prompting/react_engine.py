"""
02_react_prompting/react_engine.py
Engine ReAct (Reasoning + Acting) Mandiri dalam Python.
Mengimplementasikan loop ReAct: Thought -> Action -> Observation -> Final Answer.
"""

import re
import math
from typing import Dict, Callable, Any
from rich.console import Console
from rich.panel import Panel

console = Console()

class ReActAgentEngine:
    """Engine ReAct sederhana dengan Tool Registration dan State Management."""

    def __init__(self, max_iterations: int = 5):
        self.tools: Dict[str, Callable] = {}
        self.max_iterations = max_iterations

    def register_tool(self, name: str, func: Callable, description: str):
        """Mendaftarkan fungsi sebagai tool agen."""
        self.tools[name] = {
            "func": func,
            "description": description
        }

    def _get_tools_prompt(self) -> str:
        descriptions = []
        for name, info in self.tools.items():
            descriptions.append(f"- {name}: {info['description']}")
        return "\n".join(descriptions)

    def execute_tool(self, tool_name: str, argument: str) -> str:
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' tidak ditemukan."
        try:
            result = self.tools[tool_name]["func"](argument)
            return str(result)
        except Exception as e:
            return f"Exception saat menjalankan {tool_name}: {str(e)}"

    def run_simulated_react(self, query: str):
        """Simulasi alur ReAct untuk pertanyaan perhitungan dan pencarian."""
        console.print(Panel(f"[bold yellow]Pertanyaan User:[/bold yellow] {query}", title="ReAct Engine Runner"))
        
        # Simulasi alur berpikir ReAct
        steps = [
            {
                "thought": "Saya perlu menghitung luas lingkaran dengan radius 7 cm.",
                "action": ("calculate_area", "7"),
            },
            {
                "thought": "Hasil luas lingkaran adalah 153.94 cm^2. Sekarang saya akan mengalikannya dengan faktor 3.",
                "action": ("multiply", "153.94 * 3"),
            },
            {
                "thought": "Saya sudah memperoleh hasil perkalian 461.82. Informasi sudah lengkap.",
                "final_answer": "Luas lingkaran dengan radius 7 cm dikali 3 adalah 461.82 cm²."
            }
        ]

        history = []
        for i, step in enumerate(steps, 1):
            console.print(f"\n[bold magenta]--- Iterasi {i} ---[/bold magenta]")
            console.print(f"[yellow]Thought:[/yellow] {step['thought']}")
            
            if "action" in step:
                tool_name, arg = step["action"]
                console.print(f"[cyan]Action:[/cyan] {tool_name}({arg})")
                obs = self.execute_tool(tool_name, arg)
                console.print(f"[green]Observation:[/green] {obs}")
                history.append((step['thought'], tool_name, arg, obs))
            elif "final_answer" in step:
                console.print(f"[bold green]Final Answer:[/bold green] {step['final_answer']}")
                break

# Sample Tool Functions
def calculate_area(radius_str: str) -> float:
    r = float(radius_str)
    return round(math.pi * (r ** 2), 2)

def multiply(expr: str) -> float:
    parts = expr.split('*')
    return round(float(parts[0].strip()) * float(parts[1].strip()), 2)

def main():
    engine = ReActAgentEngine()
    engine.register_tool("calculate_area", calculate_area, "Hitung luas lingkaran dari radius (r)")
    engine.register_tool("multiply", multiply, "Kalikan dua angka dengan format 'a * b'")

    engine.run_simulated_react("Berapa luas lingkaran r=7 jika dikali 3?")

if __name__ == "__main__":
    main()
