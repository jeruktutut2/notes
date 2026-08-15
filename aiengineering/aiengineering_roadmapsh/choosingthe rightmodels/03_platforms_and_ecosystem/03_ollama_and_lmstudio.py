#!/usr/bin/env python3
"""
03_ollama_and_lmstudio.py
Modul integrasi dengan Local Model Runtimes (Ollama & LM Studio):
- Ollama REST API (`http://localhost:11434/api/generate`)
- LM Studio Local Endpoint (`http://localhost:1234/v1/chat/completions`)
- Modelfile & OpenAI-compatible compatibility layer
"""

import time
import urllib.request
import urllib.error
from typing import Dict, Any

def simulate_ollama_api_call(model: str, prompt: str) -> Dict[str, Any]:
    """Simulasi pemanggilan REST API Ollama lokal."""
    print(f"\n[OLLAMA LOCAL REST API] Calling endpoint: http://localhost:11434/api/chat")
    print(f" Model: {model} | Prompt: '{prompt}'")
    
    start = time.time()
    time.sleep(0.35)
    lat = round((time.time() - start) * 1000, 2)
    
    return {
        "model": model,
        "created_at": "2026-07-26T10:00:00Z",
        "message": {
            "role": "assistant",
            "content": f"Respons dari model Ollama lokal '{model}': Proses berjalan 100% offline di GPU lokal Anda!"
        },
        "done": True,
        "eval_count": 42,
        "eval_duration_ms": lat,
        "tokens_per_second": round(42 / (lat / 1000.0), 1)
    }

def main():
    print("=" * 65)
    print(" 🦙 OLLAMA & LM STUDIO LOCAL INFERENCE RUNTIMES")
    print("=" * 65)
    
    # Try actual Ollama check if available
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=0.5) as resp:
            if resp.status == 200:
                print("✅ Ollama Service TERDETEKSI berjalan secara live di port 11434!")
            else:
                print("ℹ️ Ollama Service tidak merespons di port 11434. Menggunakan mode simulasi.")
    except Exception:
        print("ℹ️ Ollama Service tidak aktif secara lokal. Menggunakan mode simulasi API.")

        
    res = simulate_ollama_api_call("llama3.1:8b", "Jelaskan konsep Ollama Modelfile.")
    print(f"\n💬 Content: {res['message']['content']}")
    print(f"⚡ Throughput: {res['tokens_per_second']} tokens/sec | Latensi: {res['eval_duration_ms']} ms")
    
    print("\n📋 Perbandingan Ollama vs LM Studio:")
    print("• Ollama    : CLI-first runtime, sangat ringan, ideal untuk background service & Docker containers.")
    print("• LM Studio : GUI-first desktop application, ideal untuk pengujian visual, tweaking hyperparameters, dan model inspection.")

if __name__ == "__main__":
    main()
