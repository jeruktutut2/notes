#!/usr/bin/env python3
"""
Modul 03: Building Using Frameworks
Overview & Simulasi Framework Ekosistem AI Agents:
- LangChain & LangGraph (Stateful Graph Engine)
- Haystack & LlamaIndex (Data-Centric & Pipeline Architecture)
- CrewAI & AutoGen (Role-Playing & Multi-Agent GroupChat)
- Smolagents (Smol Depot) & Agno (Code Agents & Fast Pydantic Structure)
"""

import json
from typing import Dict, Any, List

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"


def simulate_langgraph():
    print(f"\n{BOLD}{CYAN}=== 1. LANGCHAIN & LANGGRAPH (STATEFUL GRAPH ENGINE) ==={RESET}")
    print("Konsep Utama: State graph deterministik dengan nodes, conditional edges, dan state reducers.")
    
    state = {"messages": ["User: Analisis data keuangan."], "next_node": "agent"}
    print(f"  Initial Graph State: {state}")
    
    # Node 1: Agent Node
    print(f"  ⚡ Running Node [{GREEN}agent{RESET}]... Decided action: Call Vector Tool.")
    state["messages"].append("Assistant: Action -> vector_search")
    state["next_node"] = "tools"

    # Conditional Edge Check
    print(f"  🔀 Evaluating Conditional Edge from 'agent' -> Target Node: '{state['next_node']}'")

    # Node 2: Tools Node
    print(f"  ⚡ Running Node [{BLUE}tools{RESET}]... Tool executed. Result: Data ditemukan.")
    state["messages"].append("Tool: Laporan Keuangan Q2 2026 OK")
    state["next_node"] = "END"
    print(f"  ✓ Reached Graph Terminal Node [{MAGENTA}END{RESET}]")


def simulate_llamaindex_and_haystack():
    print(f"\n{BOLD}{YELLOW}=== 2. LLAMAINDEX & HAYSTACK (DATA-CENTRIC & PIPELINES) ==={RESET}")
    print("Konsep Utama: Indexing data terstruktur/tidak terstruktur dan router query engine.")

    print("  [LlamaIndex Router Query Engine]:")
    print("    • Query input: 'Berapa total pengeluaran operasional?'")
    print("    • Router Selects Engine: `SQLDatabaseQueryEngine` (karena query finansial terstruktur).")
    print("    • Executed SQL: `SELECT SUM(amount) FROM expenses WHERE category='OPEX';` -> Rp 450M.")
    
    print("  [Haystack Pipeline]:")
    print("    • Pipeline: `FileConverter` -> `PreProcessor` -> `EmbeddingRetriever` -> `PromptNode` -> `Answer`.")


def simulate_crewai_and_autogen():
    print(f"\n{BOLD}{MAGENTA}=== 3. CREWAI & AUTOGEN (MULTI-AGENT & GROUPCHAT) ==={RESET}")
    print("Konsep Utama: Agent berbasis peran (CrewAI) dan percakapan antar agent (AutoGen).")

    print("  [CrewAI Crew Process]:")
    print("    • Agent 1: `Senior Technical Writer` (Goal: Tulis dokumentasi API)")
    print("    • Agent 2: `Code QA Engineer` (Goal: Uji kebenaran sampel kode)")
    print("    • Execution Process: Sequential (Writer -> QA -> Final Output)")

    print("  [AutoGen GroupChat Manager]:")
    print("    • ConversableAgents: `UserProxyAgent`, `AssistantAgent`, `CriticAgent`")
    print("    • GroupChatManager memilih pembicara berikutnya secara otomatis berdasarkan percakapan.")


def simulate_smolagents_and_agno():
    print(f"\n{BOLD}{GREEN}=== 4. SMOLAGENTS (SMOL DEPOT) & AGNO ==={RESET}")
    print("Konsep Utama: Executing Code directly as Actions (Smolagents) & High-Performance Pydantic (Agno).")

    print("  [Smolagents (CodeAgent)]:")
    print("    • Alih-alih merespon JSON, LLM menulis skrip Python murni:")
    print(f"      {BLUE}```python\n      import math\n      res = [math.sqrt(x) for x in range(10)]\n      print(res)\n      ```{RESET}")
    print("    • Action Executed inside Secure Python Interpreter.")

    print("  [Agno Framework]:")
    print("    • Schema berbasis Pydantic `Agent(model=..., tools=[...], structured_outputs=True)`")
    print("    • Latensi sangat rendah dan overhead memori minimal.")


def main():
    print(f"{BOLD}{GREEN}===================================================={RESET}")
    print(f"{BOLD}{GREEN} MODUL 03: BUILDING USING FRAMEWORKS OVERVIEW       {RESET}")
    print(f"{BOLD}{GREEN}===================================================={RESET}")

    simulate_langgraph()
    simulate_llamaindex_and_haystack()
    simulate_crewai_and_autogen()
    simulate_smolagents_and_agno()


if __name__ == "__main__":
    main()
