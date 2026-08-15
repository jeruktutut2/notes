#!/usr/bin/env python3
"""
MODUL 5: Context Routing & Multi-Context Orchestration
Skrip 2: Context Sharding & Map-Reduce Pattern

Mendemonstrasikan:
1. Context Shard Partitioning: Memecah dokumen raksasa menjadi N bagian (shards).
2. Map Phase: Ekstraksi fakta lokal dari tiap shard secara independen/paralel.
3. Reduce Phase: Mengombinasikan hasil lokal ke dalam satu ringkasan master.
"""

from typing import List, Dict, Any

class ContextMapReducer:
    """Orchestrator Map-Reduce untuk Context Raksasa."""

    def __init__(self, shard_size_words: int = 40):
        self.shard_size_words = shard_size_words

    def create_shards(self, document_text: str) -> List[str]:
        """Map Step 0: Pemecahan dokumen menjadi shard-shard kecil."""
        words = document_text.split()
        shards = []
        for i in range(0, len(words), self.shard_size_words):
            chunk = " ".join(words[i:i + self.shard_size_words])
            shards.append(chunk)
        return shards

    def map_phase(self, shards: List[str], extraction_goal: str) -> List[Dict[str, Any]]:
        """Map Step 1: Menyiapkan prompt terisolasi untuk tiap shard."""
        mapped_results = []
        for idx, shard in enumerate(shards):
            # Simulasi ekstraksi fakta oleh LLM pada shard ini
            keywords = [w for w in shard.split() if len(w) > 6 and w.isalnum()]
            mapped_results.append({
                "shard_index": idx + 1,
                "shard_text": shard,
                "local_summary": f"Shard #{idx+1} membahas topik tentang: {', '.join(keywords[:3])}."
            })
        return mapped_results

    def reduce_phase(self, mapped_results: List[Dict[str, Any]], final_goal: str) -> str:
        """Reduce Step 2: Penggabungan hasil Map ke dalam satu context sintesis akhir."""
        local_summaries_str = "\n".join([f"- {res['local_summary']}" for res in mapped_results])

        reduced_prompt = (
            f"=== MAP-REDUCE SYNTHESIS CONTEXT ===\n"
            f"Tujuan Sintesis: {final_goal}\n\n"
            f"Hasil Ringkasan Lokal dari {len(mapped_results)} Shards:\n"
            f"{local_summaries_str}\n\n"
            f"=== INSTRUKSI REDUCE ===\n"
            f"Sintesiskan poin-poin di atas menjadi satu kesimpulan ringkas komprehensif."
        )

        return reduced_prompt

def demo():
    print("=" * 70)
    print("DEMO 2: CONTEXT SHARDING & MAP-REDUCE PATTERN")
    print("=" * 70)

    # Dokumen Raksasa Simulasi
    large_document = (
        "Bab 1: Pengenalan Arsitektur Microservices dan Keuntungannya dalam Skalabilitas Sistem Cloud. "
        "Microservices memungkinkan tim mendeploy kode secara independen tanpa mengganggu modul lain. "
        "Bab 2: Manajemen Database Terdistribusi dan Konsistensi Data menggunakan Pattern Saga. "
        "Saga pattern mengelola transaksi lintas microservices melalui event-driven orchestration. "
        "Bab 3: Keamanan API Gateway dan Rate Limiting menggunakan Token Bucket Algorithm. "
        "API Gateway bertindak sebagai entri tunggal yang menyaring traffic berbahaya dan membatasi request per detik."
    )

    map_reducer = ContextMapReducer(shard_size_words=25)

    # 1. Sharding
    shards = map_reducer.create_shards(large_document)
    print(f"Total Kata Dokumen : {len(large_document.split())} kata.")
    print(f"Jumlah Shards Dibuat: {len(shards)} shards (Ukuran per shard: ~25 kata).\n")

    # 2. Map Phase
    mapped = map_reducer.map_phase(shards, extraction_goal="Ekstrak poin penting")
    print("--- [MAP PHASE: EKSTRAKSI PARALEL LOKAL PER SHARD] ---")
    for m in mapped:
        print(f"  • {m['local_summary']}")

    # 3. Reduce Phase
    reduced_context = map_reducer.reduce_phase(mapped, final_goal="Buat Rangkuman Eksekutif Arsitektur Cloud")
    print("\n--- [REDUCE PHASE: PROMPT SINTESIS MASTER HASIL SHARDING] ---")
    print(reduced_context)
    print("=" * 70)

if __name__ == "__main__":
    demo()
