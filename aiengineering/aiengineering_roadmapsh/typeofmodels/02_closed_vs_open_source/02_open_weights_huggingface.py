#!/usr/bin/env python3
"""
Modul 02: Open Weights & Hugging Face Hub Integration
Menunjukkan cara menginspeksi metadata model open-weights,
konfigurasi arsitektur, dan struktur bobot pada Hugging Face Model Hub.
"""

import json
import urllib.request

def inspect_huggingface_model(model_id: str) -> dict:
    """
    Mengunduh metadata config model langsung dari Hugging Face API
    tanpa harus mengunduh file bobot raksasa.
    """
    api_url = f"https://huggingface.co/api/models/{model_id}"
    
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            pipeline_tag = data.get("pipeline_tag", "unknown")
            tags = data.get("tags", [])
            downloads = data.get("downloads", 0)
            likes = data.get("likes", 0)
            
            return {
                "model_id": model_id,
                "pipeline_tag": pipeline_tag,
                "downloads_last_month": downloads,
                "likes": likes,
                "tags": tags[:6],
                "status": "online"
            }
    except Exception as e:
        # Fallback offline metadata jika tidak ada koneksi internet
        return simulate_offline_model_metadata(model_id)

def simulate_offline_model_metadata(model_id: str) -> dict:
    offline_db = {
        "meta-llama/Meta-Llama-3.1-8B-Instruct": {
            "pipeline_tag": "text-generation",
            "downloads_last_month": 4200000,
            "likes": 5400,
            "tags": ["llama-3.1", "instruct", "meta", "safetensors", "transformers"],
            "license": "llama3.1"
        },
        "mistralai/Mistral-7B-Instruct-v0.3": {
            "pipeline_tag": "text-generation",
            "downloads_last_month": 2800000,
            "likes": 4100,
            "tags": ["mistral", "instruct", "apache-2.0", "safetensors"],
            "license": "apache-2.0"
        },
        "Qwen/Qwen2.5-7B-Instruct": {
            "pipeline_tag": "text-generation",
            "downloads_last_month": 3100000,
            "likes": 3900,
            "tags": ["qwen", "instruct", "apache-2.0", "code"],
            "license": "apache-2.0"
        }
    }
    
    meta = offline_db.get(model_id, {
        "pipeline_tag": "text-generation",
        "downloads_last_month": 1500000,
        "likes": 2000,
        "tags": ["open-weights", "safetensors"],
        "license": "open"
    })
    
    meta["model_id"] = model_id
    meta["status"] = "offline_simulated"
    return meta

def main():
    print("=" * 75)
    print("      INSPEKTUR MODEL OPEN-WEIGHTS HUGGING FACE HUB")
    print("=" * 75)
    
    popular_open_models = [
        "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "mistralai/Mistral-7B-Instruct-v0.3",
        "Qwen/Qwen2.5-7B-Instruct"
    ]
    
    print("Memeriksa metadata model open-weights dari Hugging Face Registry:\n")
    
    for repo in popular_open_models:
        info = inspect_huggingface_model(repo)
        print(f"📦 Model Repo : {info['model_id']}")
        print(f"   Pipeline   : {info['pipeline_tag']}")
        print(f"   Popularity : {info['downloads_last_month']:,} downloads | {info['likes']:,} likes")
        print(f"   Tags       : {', '.join(info['tags'])}")
        print(f"   Status Hub : {info['status']}\n")

    print("💡 METODE PENGGUNAAN OPEN WEIGHTS:")
    print("1. Download Weights: `git lfs clone` atau `huggingface-cli download`")
    print("2. Run Locally     : Pindah ke Ollama (`.gguf`) atau vLLM (`.safetensors`).")

if __name__ == "__main__":
    main()
