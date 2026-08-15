"""
==============================================================================
CONTOH MODUL 6C: AGENTIC AI DENGAN LANGGRAPH (IMPLEMENTASI ASLI)
==============================================================================
Modul ini adalah contoh nyata penggunaan library `langgraph` dan `langchain`.

Prasyarat (Install library terlebih dahulu jika belum):
pip install langgraph langchain-core langchain-openai

Cara Menjalankan:
1. Pastikan Anda memiliki OPENAI_API_KEY di file .env Anda.
2. Jalankan: python agent_langgraph_real.py
==============================================================================
"""

import os
from typing import Annotated, TypedDict
from dotenv import load_dotenv

# Import asli dari LangGraph dan LangChain
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
# from langchain_openai import ChatOpenAI  # <-- Buka komentar ini jika ingin pakai OpenAI
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

# ==============================================================================
# 1. DEFINISI STATE
# ==============================================================================
# Menggunakan `add_messages` agar list pesan selalu di-append otomatis oleh framework
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# ==============================================================================
# 2. DEFINISI TOOLS
# ==============================================================================
@tool
def cek_cuaca(lokasi: str) -> str:
    """Mengembalikan informasi cuaca saat ini untuk lokasi tertentu."""
    # Dummy data
    cuaca_dummy = {
        "jakarta": "31°C, Cerah Berawan",
        "bandung": "24°C, Hujan Ringan",
        "surabaya": "34°C, Panas Terik",
        "yogyakarta": "28°C, Mendung"
    }
    return cuaca_dummy.get(lokasi.lower(), f"Cuaca di {lokasi} tidak diketahui.")

tools = [cek_cuaca]

# ==============================================================================
# 3. PERSIAPAN LLM & GRAPH
# ==============================================================================

# --- OPSI 1: Menggunakan OpenAI (Non-Aktif) ---
# Jika ingin menggunakan OpenAI, pastikan OPENAI_API_KEY ada di .env dan buka komentar di bawah ini:
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# --- OPSI 2: Menggunakan Ollama Lokal (Aktif) ---
ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
if ollama_url.endswith("/api/chat"):
    ollama_url = ollama_url.replace("/api/chat", "")

llm = ChatOllama(
    model=os.getenv("DEFAULT_MODEL", "llama3.2"),
    temperature=0,
    base_url=ollama_url
)
llm_with_tools = llm.bind_tools(tools)

# Node Reasoning (LLM)
def chatbot_node(state: AgentState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# Inisialisasi Graph
graph_builder = StateGraph(AgentState)

# Tambahkan Node
graph_builder.add_node("chatbot", chatbot_node)
graph_builder.add_node("tools", ToolNode(tools)) # Node bawaan LangGraph untuk eksekusi tools

# Definisikan Alur (Edges)
graph_builder.add_edge(START, "chatbot")

# Conditional Edge: Jika LLM memanggil tool, ke node "tools". Jika tidak, ke END.
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition, 
)

# Setelah tool selesai dieksekusi, kembali ke LLM untuk merangkum hasil (Cyclical Graph)
graph_builder.add_edge("tools", "chatbot")

# Compile graf menjadi fungsi yang bisa dijalankan (Runnable)
app = graph_builder.compile()

# ==============================================================================
# 4. RUNNER SIMULATOR (CLI)
# ==============================================================================
def jalankan_langgraph_asli():
    print("=========================================================")
    print("LANGGRAPH ASLI (REAL IMPLEMENTATION)")
    print("Ketik 'keluar' untuk berhenti.")
    print("=========================================================")
    
    # Cek API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ PERINGATAN: OPENAI_API_KEY tidak ditemukan di environment.")
        print("Pastikan Anda sudah set API key sebelum mencoba chat ini.")
        print("=========================================================\n")
    
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["keluar", "exit", "quit", "q"]:
            break
            
        # Alirkan input pengguna ke Graph
        input_message = HumanMessage(content=user_input)
        
        # app.stream memungkinkan kita melihat pergerakan antar node di StateGraph
        for event in app.stream({"messages": [input_message]}):
            for node_name, node_state in event.items():
                print(f"--- [Log: Menjalankan Node {node_name.upper()}] ---")
                
                # Menampilkan aktivitas
                msg = node_state["messages"][-1]
                if isinstance(msg, AIMessage):
                    if msg.tool_calls:
                        tool_call = msg.tool_calls[0]
                        print(f"🛠️ Agent memanggil tool: '{tool_call['name']}' dengan argumen {tool_call['args']}")
                    elif msg.content:
                        print(f"🤖 AI: {msg.content}")
                elif isinstance(msg, ToolMessage):
                    print(f"📊 Hasil Tool: {msg.content}")
        print()

if __name__ == "__main__":
    jalankan_langgraph_asli()
