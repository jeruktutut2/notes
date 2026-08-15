"""
==============================================================================
CONTOH MODUL 6B: AGENTIC AI DENGAN LANGGRAPH FRAMEWORK
==============================================================================
Jika pada agent_manual.py kita membuat ReAct loop dari nol dengan regex,
pada modul ini kita mempelajari cara standar industri menggunakan **LangGraph**.

MENGAPA LANGGRAPH?
    - Stateful Graph: Mengelola State percakapan dalam struktur graf berarah.
    - Cyclical Flow: Mendukung perulangan (loop) antar node reasoning dan tool node.
    - Fault Tolerance & Checkpointing: Mudah ditambah fitur pause, resume, dan intervensi manusia.

KUMPULAN NODE & EDGES:
    [START] -> (Node Reasoning / LLM) -> Conditional Edge:
                                              |-- Butuh Tool?  --> (Node Exec Tools) --|
                                              |-- Sudah Selesai? --> [END] <-----------|

CARA PAKAI:
    - Jalankan: python agent_langgraph.py
==============================================================================
"""

import os
import json
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv

load_dotenv()

# ==============================================================================
# 1. STRUCTURAL STATE DEFINITION
# ==============================================================================
# State menyimpan seluruh memory percakapan dan status internal agent.

class AgentState(TypedDict):
    """
    State utama yang dipassing dari node ke node dalam Graf.
    messages: Daftar riwayat percakapan yang terus bertambah.
    """
    messages: list
    langkah_terakhir: str


# ==============================================================================
# 2. DEFINISI NODES (SIMULASI ALUR GRAPH SCRIPT)
# ==============================================================================

def node_reasoning_llm(state: AgentState) -> AgentState:
    """
    Node 1: Berpikir dan Mengambil Keputusan (Reasoning).
    Di dunia nyata, ini memanggil `llm.bind_tools(...)` dari LangChain/LangGraph.
    """
    print("\n🧠 [NODE REASONING] Menganalisis state dan menentukan tindakan selanjutnya...")
    messages = state.get("messages", [])
    query_terakhir = messages[-1]["content"]

    # Simulasi keputusan Agentic Graph
    if "cuaca" in query_terakhir.lower():
        state["langkah_terakhir"] = "panggil_tool_cuaca"
        messages.append({"role": "assistant", "content": "Saya perlu mengecek informasi cuaca real-time.", "tool_call": "cek_cuaca"})
    else:
        state["langkah_terakhir"] = "selesai"
        messages.append({"role": "assistant", "content": f"Jawaban langsung untuk: {query_terakhir}"})

    state["messages"] = messages
    return state


def node_eksekusi_tool(state: AgentState) -> AgentState:
    """
    Node 2: Eksekusi Tool.
    Node ini hanya berjalan jika Conditional Edge mengarahkan ke sini.
    """
    print("🛠️ [NODE EXECUTE TOOLS] Mengendalikan eksekusi alat eksternal...")
    messages = state["messages"]
    
    # Eksekusi tool cuaca dummy
    hasil_tool = {"suhu": "31°C", "kondisi": "Cerah Berawan", "kota": "Jakarta"}
    
    messages.append({"role": "tool", "content": json.dumps(hasil_tool)})
    state["messages"] = messages
    state["langkah_terakhir"] = "kembali_ke_reasoning"
    return state


# ==============================================================================
# 3. CONDITIONAL ROUTER (DECISION EDGE)
# ==============================================================================

def router_kondisional(state: AgentState) -> str:
    """
    Fungsi penentu arah (Conditional Edge):
    Menentukan apakah alur lanjut ke 'node_eksekusi_tool' atau ke 'END'.
    """
    langkah = state.get("langkah_terakhir")
    if langkah == "panggil_tool_cuaca":
        return "ke_tool"
    else:
        return "ke_end"


# ==============================================================================
# 4. SIMULATOR GRAPH RUNNER (GAYA LANGGRAPH)
# ==============================================================================

def jalankan_langgraph_agent_demo(user_input: str):
    print(f"\n=========================================================")
    print(f"RUNNING LANGGRAPH STATEFUL AGENT")
    print(f"INPUT: '{user_input}'")
    print("=========================================================")

    # Inisialisasi State Awal
    state: AgentState = {
        "messages": [{"role": "user", "content": user_input}],
        "langkah_terakhir": "start"
    }

    # Loop State Machine Graf
    max_steps = 5
    step = 0

    while step < max_steps:
        step += 1
        print(f"\n--- STEP GRAF #{step} ---")

        # 1. Jalankan Node Reasoning
        state = node_reasoning_llm(state)

        # 2. Evaluasi Conditional Edge (Router)
        tujuan = router_kondisional(state)
        print(f"🔀 Router Direction: -> '{tujuan}'")

        if tujuan == "ke_tool":
            # Jalankan Node Tool lalu putar kembali ke Reasoning
            state = node_eksekusi_tool(state)
        elif tujuan == "ke_end":
            print("\n🏁 Graf mencapai Node [END]. Siklus Selesai.")
            break

    print("\n--- [RIWAYAT AGENT STATE MESSAGES] ---")
    for m in state["messages"]:
        print(f"{m['role'].upper()}: {m['content']}")


if __name__ == "__main__":
    jalankan_langgraph_agent_demo("Bagaimana kondisi cuaca di Jakarta hari ini?")
