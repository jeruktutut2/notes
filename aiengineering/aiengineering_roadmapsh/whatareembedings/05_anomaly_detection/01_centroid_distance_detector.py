#!/usr/bin/env python3
"""
01_centroid_distance_detector.py
--------------------------------
Deteksi Anomali Data / Outlier berbasis Jarak ke Centroid Kluster Normal.
"""

import numpy as np

# Dataset Transaksi Normal Sintetis
NORMAL_TRANSACTIONS = [
    "Pembayaran belanja minimarket indomaret Rp 45.000",
    "Transfer antar bank untuk tagihan listrik Rp 250.000",
    "Topup e-wallet gopay via mobile banking Rp 100.000",
    "Pembelian kopi di cafe starbucks Rp 65.000",
    "Pembayaran langganan spotify bulanan Rp 55.000",
]

def mock_transaction_embedding(text: str, dim: int = 8) -> np.ndarray:
    t = text.lower()
    vec = np.zeros(dim)
    if any(w in t for w in ["pembayaran", "transfer", "topup", "belanja", "kopi", "spotify"]):
        vec[0:4] += 0.95
    if "hacker" in t or "bitcoin" in t or "darkweb" in t or "unknown" in t:
        vec[4:8] += 0.95
    
    seed = sum(ord(c) for c in text[:15])
    np.random.seed(seed)
    vec += np.random.uniform(-0.05, 0.05, size=dim)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec

def calculate_centroid(embeddings: list) -> np.ndarray:
    avg = np.mean(embeddings, axis=0)
    return avg / np.linalg.norm(avg)

def main():
    print("=" * 70)
    print("🚨 DEMO: ANOMALY DETECTION VIA EMBEDDING CENTROID DISTANCE")
    print("=" * 70)

    print("\n1. Meng-generate Embedding Transaksi Normal...")
    normal_embs = [mock_transaction_embedding(t) for t in NORMAL_TRANSACTIONS]
    centroid = calculate_centroid(normal_embs)
    print("   ✅ Centroid Transaksi Normal Berhasil Dihitung.")

    # Tentukan Threshold Cosine Distance (1 - CosineSimilarity)
    threshold_distance = 0.40

    test_transactions = [
        "Pembayaran makan siang di restoran Rp 120.000", # Normal
        "Transfer $50,000 USD ke rekening tidak dikenal di Darkweb Bitcoin Mixer", # Anomali!
        "Pembelian tiket bioskop XXI Rp 50.000", # Normal
    ]

    print(f"\n2. Menguji Transaksi Baru (Threshold Jarak Anomali = {threshold_distance}):")
    for tx in test_transactions:
        tx_emb = mock_transaction_embedding(tx)
        cos_sim = float(np.dot(tx_emb, centroid))
        cos_dist = 1.0 - cos_sim

        is_anomaly = cos_dist > threshold_distance
        status = "🚨 ANOMALI / FRAUD DETECTED!" if is_anomaly else "✅ NORMAL"

        print(f"\n   📝 Transaksi: \"{tx}\"")
        print(f"      • Cosine Distance to Centroid: {cos_dist:.4f}")
        print(f"      • Status                      : {status}")

    print("=" * 70)

if __name__ == "__main__":
    main()
