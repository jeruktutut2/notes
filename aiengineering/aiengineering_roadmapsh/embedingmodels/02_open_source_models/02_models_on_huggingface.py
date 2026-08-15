#!/usr/bin/env python3
"""
02_models_on_huggingface.py
Modul untuk mendemonstrasikan ekstraksi embedding dari Hugging Face Hub (BAAI/bge-small-en-v1.5)
secara manual menggunakan `transformers` (AutoTokenizer, AutoModel) dan teknik Pooling.

Roadmap: https://roadmap.sh/ai-engineer
"""

import math
import random

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

def mock_mean_pooling(dim=384):
    """Simulasi Mean Pooling PyTorch."""
    random.seed(42)
    raw = [random.gauss(0, 1) for _ in range(dim)]
    norm = math.sqrt(sum(x*x for x in raw))
    return [x / norm for x in raw]

def mock_cls_pooling(dim=384):
    """Simulasi CLS Pooling PyTorch (mengambil token pertama [CLS])."""
    random.seed(43)
    raw = [random.gauss(0, 1) for _ in range(dim)]
    norm = math.sqrt(sum(x*x for x in raw))
    return [x / norm for x in raw]

def run_huggingface_models_demo():
    print("=" * 70)
    print("     HUGGING FACE HUB MODELS & MANUAL POOLING (BGE-SMALL-EN)")
    print("=" * 70)
    
    model_id = "BAAI/bge-small-en-v1.5"
    text = "Hugging Face Hub menyediakan ribuan model embedding open source."
    
    using_hf = False
    
    try:
        import torch
        from transformers import AutoTokenizer, AutoModel
        
        print(f"📦 Loading Hugging Face Model & Tokenizer: '{model_id}'...")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModel.from_pretrained(model_id)
        
        encoded_input = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            model_output = model(**encoded_input)
            
        token_embeddings = model_output[0]
        input_mask_expanded = encoded_input['attention_mask'].unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        mean_pooled_vec = (sum_embeddings / sum_mask).squeeze().numpy()
        mean_pooled_vec = (mean_pooled_vec / np.linalg.norm(mean_pooled_vec)).tolist()
        
        cls_vec = model_output[0][:, 0].squeeze().numpy()
        cls_vec = (cls_vec / np.linalg.norm(cls_vec)).tolist()
        
        using_hf = True
        
    except Exception as e:
        print(f"ℹ️ Menggunakan simulasi PyTorch/Hugging Face ({e})...")
        mean_pooled_vec = mock_mean_pooling()
        cls_vec = mock_cls_pooling()
        
    print("\n1. Perbandingan Teknik Pooling Output Transformer:")
    print(f"   • Input Text         : '{text}'")
    print(f"   • Model Selected     : {model_id} (Top Tier MTEB Leaderboard)")
    print(f"   • Mean Pooling Vector: Dimensi {len(mean_pooled_vec)} | Head: {[round(x, 4) for x in mean_pooled_vec[:4]]}")
    print(f"   • CLS Token Vector   : Dimensi {len(cls_vec)} | Head: {[round(x, 4) for x in cls_vec[:4]]}")
    
    print("\n2. Perbedaan Mean Pooling vs CLS Pooling:")
    print("   • Mean Pooling: Merata-ratakan seluruh token dalam kalimat -> Sangat direkomendasikan untuk Semantic Search.")
    print("   • CLS Pooling : Mengambil representasi token [CLS] awal -> Cocok untuk beberapa arsitektur klasifikasi.")
    
    print("\n💡 Key Takeaway AI Engineer:")
    print("   Model dari Hugging Face Hub (seperti `BAAI/bge-small-en-v1.5`) secara konsisten mengalahkan")
    print("   banyak model proprietary di MTEB Leaderboard, dan dapat dijalankan sepenuhnya secara lokal!\n")

if __name__ == "__main__":
    run_huggingface_models_demo()
