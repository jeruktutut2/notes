#!/usr/bin/env python3
"""
02_zero_shot_classification.py
------------------------------
Klasifikasi Zero-Shot Berbasis Kemiripan Cosine Embedding Label vs Teks.
Tanpa training data / tanpa fit model!
"""

import numpy as np

LABELS = [
    {"category": "Politik & Pemerintahan", "desc": "Berita pemilu, kebijakan menteri, perundang-undangan DPR, dan diplomasi antar negara."},
    {"category": "Olahraga & Sepakbola", "desc": "Pertandingan liga sepakbola, turnamen bulutangkis, skor pertandingan, dan atlet juara."},
    {"category": "Teknologi & Sains", "desc": "Inovasi komputer, peluncuran smartphone, kecerdasan buatan AI, dan penemuan luar angkasa."},
    {"category": "Kuliner & Resep", "desc": "Resep makanan lezat, restoran enak, kue tradisional, dan tips memasak di dapur."},
]

def mock_embedding(text: str, dim: int = 16) -> np.ndarray:
    t = text.lower()
    vec = np.zeros(dim)
    if any(w in t for w in ["politik", "pemilu", "dpr", "menteri", "pemerintah", "kebijakan"]):
        vec[0:4] += 0.9
    if any(w in t for w in ["olahraga", "sepakbola", "liga", "juara", "pemain", "gol", "lapangan"]):
        vec[4:8] += 0.9
    if any(w in t for w in ["teknologi", "komputer", "ai", "smartphone", "aplikasi", "sains"]):
        vec[8:12] += 0.9
    if any(w in t for w in ["kuliner", "resep", "makanan", "restoran", "memasak", "dapur"]):
        vec[12:16] += 0.9
    
    seed = sum(ord(c) for c in text[:15])
    np.random.seed(seed)
    vec += np.random.uniform(-0.05, 0.05, size=dim)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec

def zero_shot_classify(text: str):
    text_emb = mock_embedding(text)
    scores = []
    for item in LABELS:
        label_emb = mock_embedding(item["category"] + " " + item["desc"])
        sim = float(np.dot(text_emb, label_emb))
        scores.append((item["category"], sim))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

def main():
    print("=" * 70)
    print("🎯 DEMO: ZERO-SHOT TEXT CLASSIFICATION VIA EMBEDDINGS")
    print("=" * 70)

    test_articles = [
        "Timnas Indonesia berhasil mencetak gol kemenangan di menit akhir pertandingan liga.",
        "Menteri Keuangan merilis kebijakan insentif pajak baru untuk sektor industri.",
        "Model AI terbaru mampu menghasilkan kode pemrograman otomatis dengan efisiensi tinggi.",
    ]

    for article in test_articles:
        print(f"\n📰 Artikel: \"{article}\"")
        scores = zero_shot_classify(article)
        top_cat, top_sim = scores[0]
        print(f"   🏆 Klasifikasi Zero-Shot: [{top_cat}] (Similarity: {top_sim:.4f})")
        print("   📊 Perbandingan Skor Kategori:")
        for cat, sim in scores:
            print(f"      • {cat:<25} : {sim:.4f}")

    print("=" * 70)

if __name__ == "__main__":
    main()
