#!/usr/bin/env python3
"""
Modul 4: Embeddings and Vector Search Simulator
Simulasi perhitungan matematika Vektor Embedding, Metrik Keserupaan (Cosine Similarity, Dot Product, Euclidean Distance),
dan perbandingan Semantic Search vs Lexical Keyword Search.
"""

import math
from dataclasses import dataclass
from typing import List, Tuple

# ANSI Colors
HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Simulating Synthetic Embedding Vector (5 Dimensions for readability)
# Concept dimensions: [Kucing/Hewan, Teknologi/AI, Finansial, Makanan, Medis]
MOCK_EMBEDDINGS = {
    "Kucing Persia berbulu lebat": [0.92, 0.05, 0.01, 0.15, 0.02],
    "Anjing Golden Retriever setia": [0.88, 0.08, 0.02, 0.12, 0.03],
    "Model Pembelajaran AI Agent": [0.10, 0.95, 0.40, 0.02, 0.05],
    "Arsitektur Transformer Neural Net": [0.08, 0.98, 0.25, 0.01, 0.02],
    "Resep Sup Ayam Lezat": [0.05, 0.02, 0.01, 0.96, 0.10],
    "Vaksin Medis dan Kesehatan": [0.03, 0.10, 0.05, 0.12, 0.94],
}

def dot_product(v1: List[float], v2: List[float]) -> float:
    """Menghitung perkalian titik (Dot Product) dua vektor."""
    return sum(x * y for x, y in zip(v1, v2))

def magnitude(v: List[float]) -> float:
    """Menghitung panjang/norm L2 dari vektor."""
    return math.sqrt(sum(x * x for x in v))

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Menghitung Cosine Similarity: (v1 . v2) / (||v1|| * ||v2||)"""
    mag1 = magnitude(v1)
    mag2 = magnitude(v2)
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot_product(v1, v2) / (mag1 * mag2)

def euclidean_distance(v1: List[float], v2: List[float]) -> float:
    """Menghitung Jarak Euclidean (L2 Distance): sqrt(sum((x_i - y_i)^2))"""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(v1, v2)))

def run_demo():
    print(f"\n{BOLD}{HEADER}=== EMBEDDINGS AND VECTOR SEARCH LABORATORY ==={RESET}\n")
    print(f"{CYAN}Membandingkan pencarian semantik vektor dengan 5 dimensi konsep mock.{RESET}\n")

    # Sample Query
    query_text = "Hewan peliharaan yang lucu dan menggemaskan"
    # Query vector: dominan di Dimensi 0 (Hewan) -> [0.90, 0.02, 0.00, 0.10, 0.01]
    query_vec = [0.90, 0.02, 0.00, 0.10, 0.01]

    print(f"📌 {BOLD}Query Input:{RESET} \"{query_text}\"")
    print(f"🔢 {BOLD}Query Vector (5D):{RESET} {query_vec}\n")

    print(f"{'='*75}\n")
    print(f"{BOLD}[ 1. PENCARIAN SEMANTIK MENGGUNAKAN VECTOR METRICS ]{RESET}\n")

    results: List[Tuple[str, float, float, float]] = []

    for doc_title, doc_vec in MOCK_EMBEDDINGS.items():
        cos_sim = cosine_similarity(query_vec, doc_vec)
        dot_p = dot_product(query_vec, doc_vec)
        euc_d = euclidean_distance(query_vec, doc_vec)
        results.append((doc_title, cos_sim, dot_p, euc_d))

    # Urutkan berdasarkan Cosine Similarity tertinggi
    results.sort(key=lambda x: x[1], reverse=True)

    print(f"┌─────────────────────────────────────┬──────────────────┬──────────────┬─────────────────┐")
    print(f"│ Dokumen                             │ Cosine Sim (0-1) │ Dot Product  │ Euclidean Dist  │")
    print(f"├─────────────────────────────────────┼──────────────────┼──────────────┼─────────────────┤")
    
    for title, cos_sim, dot_p, euc_d in results:
        cos_color = GREEN if cos_sim > 0.8 else (YELLOW if cos_sim > 0.4 else RED)
        print(f"│ {title:<35} │ {cos_color}{cos_sim:<16.4f}{RESET} │ {dot_p:<12.4f} │ {euc_d:<15.4f} │")
    print(f"└─────────────────────────────────────┴──────────────────┴──────────────┴─────────────────┘")

    print(f"\n{'='*75}\n")
    print(f"{BOLD}[ 2. COMPARISON: SEMANTIC SEARCH VS LEXICAL KEYWORD SEARCH ]{RESET}\n")

    keyword_query = "Hewan peliharaan"
    print(f"Query Kata Kunci: \"{keyword_query}\"\n")

    print(f"{BOLD}A. Lexical Keyword Matching (Exact Word Match):{RESET}")
    lexical_matches = [doc for doc in MOCK_EMBEDDINGS.keys() if "hewan" in doc.lower() or "peliharaan" in doc.lower()]
    print(f"  • Hasil Keyword Matching: {RED}{lexical_matches if lexical_matches else '0 Dokumen Ditemukan! (Gagal karena tidak ada kata harfiah)'}{RESET}")

    print(f"\n{BOLD}B. Vector Semantic Search (Idea / Concept Matching):{RESET}")
    print(f"  • Top-1 Relevant Doc : {GREEN}\"{results[0][0]}\"{RESET} (Cosine Sim: {results[0][1]:.4f})")
    print(f"  • Top-2 Relevant Doc : {GREEN}\"{results[1][0]}\"{RESET} (Cosine Sim: {results[1][1]:.4f})")
    print(f"  {YELLOW}👉 Berhasil menemukan dokumen 'Kucing' & 'Anjing' meskipun kata 'hewan' tidak muncul di judul!{RESET}")

    print(f"\n{BOLD}[ RINGKASAN FORMULA PENTING ]{RESET}")
    print(" 1. Cosine Similarity  : Mengukur SUDUT antar vektor (Independen dari panjang teks).")
    print(" 2. Dot Product        : Identik dengan Cosine Sim jika vektor sudah TER-NORMALISASI (magnitudo = 1.0).")
    print(" 3. Euclidean Distance : Mengukur JARAK LURUS fisik titik (Makin KECIL nilai = Makin SERUPA).")

if __name__ == "__main__":
    run_demo()
