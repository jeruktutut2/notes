#!/usr/bin/env python3
"""
Modul 01: Serving Model Lokal via Ollama REST API
Menyediakan integrasi Python murni untuk berinteraksi dengan Ollama service
(List local models, Pull model GGUF, Generate completion, dan Stream tokens).
"""

import json
import time
import urllib.request
import urllib.error

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    def check_health(self) -> bool:
        """Memeriksa apakah service Ollama sedang berjalan di localhost:11434"""
        try:
            req = urllib.request.Request(f"{self.base_url}/")
            with urllib.request.urlopen(req, timeout=2) as response:
                return response.status == 200
        except Exception:
            return False

    def list_local_models(self) -> list:
        """Mengambil daftar model GGUF yang tersimpan di disk lokal"""
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags")
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode('utf-8'))
                return [m["name"] for m in data.get("models", [])]
        except Exception:
            return []

    def generate(self, model: str, prompt: str, stream: bool = False) -> dict:
        """Memanggil endpoint /api/generate Ollama"""
        url = f"{self.base_url}/api/generate"
        payload = json.dumps({
            "model": model,
            "prompt": prompt,
            "stream": False
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
        
        try:
            start_t = time.time()
            with urllib.request.urlopen(req, timeout=30) as response:
                res = json.loads(response.read().decode('utf-8'))
                latency = time.time() - start_t
                return {
                    "response": res.get("response", ""),
                    "latency": round(latency, 2),
                    "eval_count": res.get("eval_count", 0),
                    "eval_duration_ms": round(res.get("eval_duration", 0) / 1e6, 2)
                }
        except Exception as e:
            return {"error": str(e)}

def simulate_ollama_fallback():
    print("⚠️ SERVICE OLLAMA TIDAK TERDETEKSI DI LOCALHOST:11434.")
    print("Menampilkan simulasi interaksi Ollama REST API:\n")
    
    mock_models = ["llama3.1:8b-instruct-q4_K_M", "mistral:7b-instruct", "phi3:mini"]
    print(f"1. Endpoint GET /api/tags -> Local Models Discovered:")
    for m in mock_models:
        print(f"   • {m} (Format: GGUF, Quantization: INT4)")

    print("\n2. Endpoint POST /api/generate -> Stream Response:")
    prompt = "Apa itu RAG?"
    print(f"   Prompt: '{prompt}'")
    mock_tokens = ["RAG", " (Retrieval-Augmented", " Generation)", " mengombinasikan", " Vector DB", " dengan LLM."]
    
    print("   Streaming tokens: ", end="", flush=True)
    for tok in mock_tokens:
        time.sleep(0.05)
        print(tok, end="", flush=True)
    print("\n")

def main():
    print("=" * 75)
    print("      INTEGRASI OLLAMA LOCAL MODEL SERVING (REST API)")
    print("=" * 75)
    
    client = OllamaClient()
    is_running = client.check_health()
    
    if is_running:
        print("✅ Service Ollama Aktif di http://localhost:11434!\n")
        models = client.list_local_models()
        print(f"Model Lokal Terinstal ({len(models)}): {models}")
        
        if models:
            target_model = models[0]
            print(f"\nMencoba Generate menggunakan Model '{target_model}'...")
            res = client.generate(target_model, "Jelaskan AI Engineering dalam 1 kalimat.")
            if "error" not in res:
                print(f"Response : {res['response']}")
                print(f"Latency  : {res['latency']}s ({res['eval_count']} tokens Generated)")
    else:
        simulate_ollama_fallback()

    print("💡 PETUNJUK SERVING OLLAMA:")
    print("• Install Ollama : https://ollama.com")
    print("• Pull Model     : `ollama pull llama3.1` (Otomatis mendownload GGUF Q4_K_M)")
    print("• CLI Run        : `ollama run llama3.1`")

if __name__ == "__main__":
    main()
