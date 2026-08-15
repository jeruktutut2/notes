"""
Modul 01: Persiapan Dataset & Formatting
Skrip 2: Data Cleaning, Deduplication & Quality Filtering
"""

import hashlib

def deduplicate_dataset(dataset):
    """
    Menghapus duplikasi berdasarkan hash teks prompt + output.
    """
    seen_hashes = set()
    unique_data = []
    
    for item in dataset:
        content_str = f"{item.get('prompt', '')}|{item.get('response', '')}"
        content_hash = hashlib.md5(content_str.encode('utf-8')).hexdigest()
        
        if content_hash not in seen_hashes:
            seen_hashes.add(content_hash)
            unique_data.append(item)
            
    return unique_data

def filter_by_length(dataset, min_chars=10, max_chars=500):
    """
    Filter data yang terlalu pendek (biasanya sampah/uninformative) atau terlalu panjang.
    """
    filtered = []
    for item in dataset:
        resp_len = len(item.get('response', ''))
        if min_chars <= resp_len <= max_chars:
            filtered.append(item)
    return filtered

def demo_cleaning():
    print("=" * 60)
    print("MODUL 01 - SKRIP 2: Data Cleaning & Quality Filtering")
    print("=" * 60)
    
    raw_dataset = [
        {"prompt": "Halo", "response": "Halo! Ada yang bisa dibantu?"},
        {"prompt": "Apa itu PyTorch?", "response": "PyTorch adalah framework deep learning open source buatan Meta AI."},
        {"prompt": "Halo", "response": "Halo! Ada yang bisa dibantu?"}, # Duplikat
        {"prompt": "Tes", "response": "ok"}, # Terlalu pendek
        {"prompt": "Jelaskan RAG", "response": "RAG (Retrieval-Augmented Generation) menggabungkan vector search dengan LLM..."}
    ]
    
    print(f"Jumlah sampel awal: {len(raw_dataset)}")
    
    # 1. Deduplikasi
    deduped = deduplicate_dataset(raw_dataset)
    print(f"Jumlah sampel setelah Deduplikasi Hash: {len(deduped)}")
    
    # 2. Length Filtering
    cleaned = filter_by_length(deduped, min_chars=10, max_chars=300)
    print(f"Jumlah sampel setelah Filtering Panjang Respon: {len(cleaned)}")
    
    print("\n--- Hasil Dataset Bersih & Siap Fine-Tuning ---")
    for i, item in enumerate(cleaned, 1):
        print(f"{i}. Prompt: '{item['prompt']}' | Respon: '{item['response']}'")

if __name__ == "__main__":
    demo_cleaning()
