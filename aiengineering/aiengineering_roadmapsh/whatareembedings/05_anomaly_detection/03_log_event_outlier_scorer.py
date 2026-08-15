#!/usr/bin/env python3
"""
03_log_event_outlier_scorer.py
------------------------------
Skoring Outlier Log Event Sistem secara real-time berbasis Jarak Vektor KNN.
"""

import numpy as np

NORMAL_LOGS = [
    "HTTP 200 OK GET /api/v1/user/profile 45ms",
    "HTTP 200 OK POST /api/v1/auth/login 120ms",
    "HTTP 200 OK GET /api/v1/products 30ms",
    "HTTP 200 OK GET /health 5ms",
]

def mock_log_embed(text: str, dim: int = 8) -> np.ndarray:
    t = text.lower()
    vec = np.zeros(dim)
    if "200 ok" in t or "get" in t or "post" in t:
        vec[0:4] += 0.90
    if "500 internal" in t or "overflow" in t or "injection" in t or "unauthorized" in t:
        vec[4:8] += 0.90
    
    seed = sum(ord(c) for c in text[:15])
    np.random.seed(seed)
    vec += np.random.uniform(-0.05, 0.05, size=dim)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec

def compute_knn_outlier_score(new_log: str, k: int = 2):
    log_emb = mock_log_embed(new_log)
    normal_embs = [mock_log_embed(l) for l in NORMAL_LOGS]

    # Calculate Euclidean distances to all normal logs
    distances = [float(np.linalg.norm(log_emb - n_emb)) for n_emb in normal_embs]
    distances.sort()

    # Average distance to K nearest neighbors
    knn_score = float(np.mean(distances[:k]))
    return knn_score

def main():
    print("=" * 70)
    print("📋 DEMO: LOG EVENT OUTLIER SCORER VIA KNN DISTANCE")
    print("=" * 70)

    incoming_logs = [
        "HTTP 200 OK GET /api/v1/orders 50ms",                           # Normal
        "HTTP 500 Internal Server Error: StackOverflowException at Line 42", # Critical Outlier!
        "HTTP 401 Unauthorized: SQL Injection Pattern Detected in Query",    # Security Outlier!
    ]

    print(f"\nBaseline Logs Normal: {len(NORMAL_LOGS)} events.")
    print("\nSkoring Log Baru (KNN Outlier Score > 0.50 = Anomali/Alert):")

    for log_str in incoming_logs:
        score = compute_knn_outlier_score(log_str)
        is_alert = score > 0.50
        flag = "🚨 ALERT CRITICAL" if is_alert else "✅ NORMAL"

        print(f"\n   📄 Log Event: \"{log_str}\"")
        print(f"      • KNN Outlier Score : {score:.4f}")
        print(f"      • Status             : {flag}")

    print("=" * 70)

if __name__ == "__main__":
    main()
