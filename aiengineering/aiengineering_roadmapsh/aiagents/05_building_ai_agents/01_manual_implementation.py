"""
05_building_ai_agents/01_manual_implementation.py
Membangun AI Agent secara Manual dari Nol (Pure Python Zero-Framework Loop).
"""

import json
from typing import List, Dict, Any, Callable
from rich.console import Console
from rich.panel import Panel

console = Console()

class ManualAgentState:
    """State Machine sederhana untuk melacak memory percakapan dan status agen."""
    def __init__(self, system_prompt: str):
        self.messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system_prompt}
        ]
        self.is_completed = False

    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str, tool_calls: List[Dict[str, Any]] = None):
        msg = {"role": "assistant", "content": content}
        if tool_calls:
            msg["tool_calls"] = tool_calls
        self.messages.append(msg)

    def add_tool_result(self, tool_call_id: str, output: str):
        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": output
        })

class ManualAIAgent:
    """Implementasi Manual Agent dengan Loop while mandiri."""
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.tool_registry: Dict[str, Callable] = {}

    def register_tool(self, name: str, func: Callable):
        self.tool_registry[name] = func

    def _mock_llm_reasoning_step(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulasi respon LLM di setiap iterasi."""
        turn_count = len([m for m in messages if m["role"] == "assistant"])
        
        if turn_count == 0:
            # Model memutuskan memanggil tool
            return {
                "content": "Saya perlu memeriksa isi file data.txt untuk menjawab pertanyaan user.",
                "tool_calls": [
                    {
                        "id": "call_manual_001",
                        "function": {
                            "name": "read_file",
                            "arguments": json.dumps({"filepath": "data.txt"})
                        }
                    }
                ]
            }
        else:
            # Model memiliki cukup informasi untuk memberikan jawaban akhir
            return {
                "content": "Berdasarkan isi data.txt, status server saat ini adalah ONLINE dengan beban CPU 22%.",
                "tool_calls": None
            }

    def run(self, user_goal: str, max_turns: int = 5):
        console.print(Panel(f"[bold cyan]Manual Implementation Agent[/bold cyan]\nGoal: '{user_goal}'", title="Zero-Framework Agent"))
        
        state = ManualAgentState(self.system_prompt)
        state.add_user_message(user_goal)

        turn = 0
        while turn < max_turns and not state.is_completed:
            turn += 1
            console.print(f"\n[yellow]--- Iterasi Turn {turn} ---[/yellow]")

            # 1. Kirim state ke LLM Reasoning Engine
            response = self._mock_llm_reasoning_step(state.messages)
            console.print(f"🤖 [LLM Response]: {response['content']}")

            # 2. Periksa apakah LLM meminta Tool Calling
            tool_calls = response.get("tool_calls")
            if tool_calls:
                state.add_assistant_message(response["content"], tool_calls)
                
                for call in tool_calls:
                    call_id = call["id"]
                    func_name = call["function"]["name"]
                    args = json.loads(call["function"]["arguments"])
                    
                    console.print(f"⚙️ [Tool Dispatcher]: Memanggil '{func_name}' dengan argumen {args}")
                    
                    if func_name in self.tool_registry:
                        result = self.tool_registry[func_name](**args)
                    else:
                        result = f"Error: Tool {func_name} tidak ditemukan."
                    
                    console.print(f"📥 [Tool Output]: {result}")
                    state.add_tool_result(call_id, str(result))
            else:
                # 3. Jawaban Akhir (Completed)
                state.add_assistant_message(response["content"])
                state.is_completed = True
                console.print(f"\n[bold green]✅ Agent Selesai! Final Output:[/bold green]\n{response['content']}")

def mock_read_file(filepath: str) -> str:
    return "SERVER_STATUS: ONLINE, CPU_USAGE: 22%, MEMORY_USED: 4.2GB/16GB"

def main():
    agent = ManualAIAgent("DevOps-Manual-Agent", "Anda adalah asisten operasi server.")
    agent.register_tool("read_file", mock_read_file)
    agent.run("Berapa beban CPU server saat ini?")

if __name__ == "__main__":
    main()
