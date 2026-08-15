#!/usr/bin/env python3
"""
01_huggingface_hub_and_tasks.py
Modul eksplorasi ekosistem Hugging Face:
- Hugging Face Tasks (Taksonomi standar ML)
- Hugging Face Hub (Model discovery & metadata inspection)
- Model Cards, Licenses, & Quantization formats (GGUF, AWQ, Safetensors)
"""

import time
from typing import Dict, List, Any

def demonstrate_hf_tasks() -> List[Dict[str, str]]:
    """Taksonomi standar Hugging Face Tasks."""
    return [
        {"task": "text-generation", "pipeline": "LLM text completion (Llama 3, DeepSeek, Qwen)", "domain": "NLP"},
        {"task": "text-classification", "pipeline": "Sentiment analysis, spam detection (BERT, RoBERTa)", "domain": "NLP"},
        {"task": "feature-extraction", "pipeline": "Text embeddings for RAG (bge-large-en, e5-mistral)", "domain": "NLP"},
        {"task": "image-to-text", "pipeline": "Vision-Language OCR & captioning (Qwen2-VL, Llava)", "domain": "Multimodal"},
        {"task": "automatic-speech-recognition", "pipeline": "Audio to text transcription (Whisper V3)", "domain": "Audio"}
    ]

def simulate_hf_hub_model_lookup(model_id: str) -> Dict[str, Any]:
    """Simulasi pencarian metadata model dari Hugging Face Hub."""
    print(f"\n🔍 Searching Hugging Face Hub for: '{model_id}'...")
    time.sleep(0.3)
    
    mock_registry = {
        "meta-llama/Meta-Llama-3.1-8B-Instruct": {
            "author": "meta-llama",
            "license": "llama3.1",
            "downloads_30d": 1420000,
            "tags": ["text-generation", "safetensors", "conversational", "en", "id"],
            "pipeline_tag": "text-generation"
        },
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B": {
            "author": "deepseek-ai",
            "license": "mit",
            "downloads_30d": 980000,
            "tags": ["reasoning", "cot", "qwen", "safetensors"],
            "pipeline_tag": "text-generation"
        }
    }
    
    data = mock_registry.get(model_id, {
        "author": model_id.split('/')[0] if '/' in model_id else "unknown",
        "license": "apache-2.0",
        "downloads_30d": 500000,
        "tags": ["text-generation", "gguf"],
        "pipeline_tag": "text-generation"
    })
    
    return {
        "model_id": model_id,
        "metadata": data
    }

def main():
    print("=" * 65)
    print(" 🤗 HUGGING FACE HUB & TASKS TAXONOMY EXPLORER")
    print("=" * 65)
    
    print("\n📌 Standard Hugging Face Tasks Taxonomy:")
    tasks = demonstrate_hf_tasks()
    for t in tasks:
        print(f" • [{t['domain']:<10}] Task: {t['task']:<30} ➔ {t['pipeline']}")
        
    print("\n🔍 Fetching Model Metadata from HF Hub:")
    target_models = [
        "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
    ]
    
    for m in target_models:
        info = simulate_hf_hub_model_lookup(m)
        meta = info["metadata"]
        print(f"\n📦 Model: {info['model_id']}")
        print(f"   • License: {meta['license']} | Downloads (30d): {meta['downloads_30d']:,}")
        print(f"   • Tags: {', '.join(meta['tags'])}")

if __name__ == "__main__":
    main()
