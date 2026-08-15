#!/usr/bin/env python3
"""
01_embedding_intent_classifier.py
---------------------------------
Klasifikasi Intent/Kategori Customer Support menggunakan Embedding + Logistic Regression.
"""

import numpy as np
from sklearn.linear_model import LogisticRegression

# Dataset Training Sintetis Customer Service (Teks -> Label)
TRAIN_DATA = [
    ("Saya ingin minta refund pembayaran kemarin", "billing_refund"),
    ("Tolong kembalikan uang transaksi salah potong saldo", "billing_refund"),
    ("Bisakah saya batalkan pesanan dan dapatkan pengembalian uang?", "billing_refund"),
    ("Aplikasi error tidak bisa dibuka setelah update", "tech_support"),
    ("Layar smartphone berkedip dan crash saat login", "tech_support"),
    ("Koneksi internet terputus dan server timeout", "tech_support"),
    ("Kapan barang pesanan saya sampai ke alamat tujuan?", "shipping_tracking"),
    ("Berapa nomor resi paket pengiriman JNE saya?", "shipping_tracking"),
    ("Lacak lokasi kurir pengirim barang sekarang", "shipping_tracking"),
]

def mock_get_embedding(text: str, dim: int = 16) -> np.ndarray:
    """Mock embedding generator berdasarkan bobot kata kunci semantik."""
    text_lower = text.lower()
    vec = np.zeros(dim)
    
    if any(w in text_lower for w in ["refund", "uang", "potong", "saldo", "pembayaran", "kembalikan"]):
        vec[0:4] += [0.9, 0.1, 0.0, 0.0]
    if any(w in text_lower for w in ["error", "crash", "bug", "layar", "timeout", "update"]):
        vec[4:8] += [0.0, 0.9, 0.1, 0.0]
    if any(w in text_lower for w in ["sampai", "resi", "paket", "kurir", "lacak", "pengiriman"]):
        vec[8:12] += [0.0, 0.0, 0.9, 0.1]
    
    # Hash fallback noise
    seed = sum(ord(c) for c in text[:15])
    np.random.seed(seed)
    vec += np.random.uniform(-0.05, 0.05, size=dim)
    
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec

def main():
    print("=" * 70)
    print("🏷️ DEMO: EMBEDDING-BASED INTENT CLASSIFIER")
    print("=" * 70)

    # 1. Generate Training Embeddings
    print("\n1. Meng-generate Vektor Embedding Data Training...")
    X_train = np.array([mock_get_embedding(t) for t, l in TRAIN_DATA])
    y_train = np.array([l for t, l in TRAIN_DATA])

    # 2. Latih Logistic Regression Classifier
    print("2. Melatih Logistic Regression Classifier di atas ruang vektor...")
    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    print("   ✅ Pelatihan Selesai secara Instant!")

    # 3. Uji pada Teks Baru (Unseen Data)
    test_queries = [
        "Tagihan saya double deduction, mohon kembalikan dana",
        "Paket belum tiba padahal sudah 3 hari",
        "Aplikasi force close ketika klik tombol bayar"
    ]

    print("\n3. Pengujian Teks Baru (Unseen Customer Queries):")
    for q in test_queries:
        q_emb = mock_get_embedding(q).reshape(1, -1)
        pred_label = clf.predict(q_emb)[0]
        probs = clf.predict_proba(q_emb)[0]
        max_prob = np.max(probs)

        print(f"\n   📩 Query: \"{q}\"")
        print(f"   🎯 Prediksi Intent : [{pred_label.upper()}] (Confidence: {max_prob*100:.1f}%)")

    print("=" * 70)

if __name__ == "__main__":
    main()
