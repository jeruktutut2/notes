"""
02_drift_and_feedback_monitor.py
--------------------------------
Lab runnable untuk mensimulasikan pemantauan Data/Embedding Drift dan
Pengumpulan User Feedback (Thumbs Up / Down) dalam aplikasi LLM produksi.
"""

import time
import random
from typing import List, Dict, Any

class ProductionDriftAndFeedbackMonitor:
    """Monitoring Drift dan Feedback Pengguna"""

    def __init__(self):
        self.feedback_logs: List[Dict[str, Any]] = []
        # Simulated baseline centroid embedding vector (8-dim)
        self.baseline_query_vector = [0.12, 0.45, -0.22, 0.88, 0.05, -0.31, 0.74, 0.19]

    def log_user_feedback(self, trace_id: str, rating: int, comment: str = ""):
        """
        rating: +1 (Thumbs Up), -1 (Thumbs Down)
        """
        record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "trace_id": trace_id,
            "rating": rating,
            "comment": comment
        }
        self.feedback_logs.append(record)

    def calculate_csat_metrics(self) -> Dict[str, Any]:
        """Menghitung CSAT (Customer Satisfaction Score) dan Thumbs Up Ratio"""
        if not self.feedback_logs:
            return {"total_feedback": 0, "thumbs_up": 0, "thumbs_down": 0, "satisfaction_rate_pct": 0.0}

        total = len(self.feedback_logs)
        up = sum(1 for f in self.feedback_logs if f["rating"] > 0)
        down = sum(1 for f in self.feedback_logs if f["rating"] < 0)
        satisfaction_pct = round((up / total) * 100, 2)

        return {
            "total_feedback": total,
            "thumbs_up": up,
            "thumbs_down": down,
            "satisfaction_rate_pct": satisfaction_pct
        }

    def simulate_embedding_drift_check(self, current_batch_vectors: List[List[float]]) -> Dict[str, Any]:
        """
        Menghitung pergeseran rata-rata cosine distance dari baseline vector
        """
        drift_scores = []
        for vec in current_batch_vectors:
            # Cosine similarity simulation
            dot_prod = sum(a * b for a, b in zip(self.baseline_query_vector, vec))
            mag_a = sum(a**2 for a in self.baseline_query_vector) ** 0.5
            mag_b = sum(b**2 for b in vec) ** 0.5
            similarity = dot_prod / (mag_a * mag_b) if (mag_a * mag_b) > 0 else 0
            drift_distance = 1.0 - similarity
            drift_scores.append(drift_distance)

        avg_drift = sum(drift_scores) / len(drift_scores) if drift_scores else 0.0
        drift_detected = avg_drift > 0.35  # Threshold drift 0.35

        return {
            "average_drift_distance": round(avg_drift, 4),
            "drift_detected": drift_detected,
            "alert_status": "⚠️ ALERT: Embedding Data Drift Detected!" if drift_detected else "✅ Normal - Query distribution stable."
        }

def main():
    print(f"\n=======================================================")
    print(f"📈 DRIFT DETECTION & USER FEEDBACK MONITORING LAB")
    print(f"=======================================================\n")

    monitor = ProductionDriftAndFeedbackMonitor()

    # Part 1: Log Feedback
    print("--- 1. SIMULASI LOG USER FEEDBACK ---")
    monitor.log_user_feedback("tr-101", rating=1, comment="Sangat membantu!")
    monitor.log_user_feedback("tr-102", rating=1, comment="Respon cepat")
    monitor.log_user_feedback("tr-103", rating=-1, comment="Jawaban tidak relevan")
    monitor.log_user_feedback("tr-104", rating=1, comment="Bagus")
    monitor.log_user_feedback("tr-105", rating=1, comment="Lengkap")

    csat = monitor.calculate_csat_metrics()
    print(f"Total Feedback Received : {csat['total_feedback']}")
    print(f"Thumbs Up 👍           : {csat['thumbs_up']}")
    print(f"Thumbs Down 👎         : {csat['thumbs_down']}")
    print(f"Satisfaction Rate       : {csat['satisfaction_rate_pct']}%\n")

    # Part 2: Embedding Drift Check
    print("--- 2. SIMULASI EMBEDDING DATA DRIFT ---")
    
    # Normal Batch (Queries similar to baseline)
    normal_batch = [
        [0.10, 0.42, -0.20, 0.85, 0.04, -0.30, 0.70, 0.18],
        [0.14, 0.48, -0.25, 0.90, 0.06, -0.33, 0.76, 0.20]
    ]
    res_normal = monitor.simulate_embedding_drift_check(normal_batch)
    print(f"Batch 1 (Normal Queries)  - Drift Score: {res_normal['average_drift_distance']} -> {res_normal['alert_status']}")

    # Shifted Batch (Queries on completely new topic/language shift)
    shifted_batch = [
        [-0.85, 0.10, 0.90, -0.40, 0.70, 0.88, -0.10, -0.60],
        [-0.90, 0.05, 0.95, -0.45, 0.75, 0.92, -0.15, -0.65]
    ]
    res_shifted = monitor.simulate_embedding_drift_check(shifted_batch)
    print(f"Batch 2 (Shifted Queries) - Drift Score: {res_shifted['average_drift_distance']} -> {res_shifted['alert_status']}\n")

    print("✅ Drift & feedback monitoring lab selesai!")

if __name__ == "__main__":
    main()
