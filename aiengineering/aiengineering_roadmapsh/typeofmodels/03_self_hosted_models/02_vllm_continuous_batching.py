#!/usr/bin/env python3
"""
Modul 02: Arsitektur vLLM, PagedAttention & Continuous Batching
Simulasi visual bagaimana engine inferensi produksi (vLLM) mengelola memori KV Cache
secara efisien dan menyisipkan request baru tanpa menunggu batch lama selesai.
"""

import time

def simulate_naive_batching():
    """
    Naive Batching (Static Batching):
    Harus menunggu semua request dalam 1 batch selesai generate token sebelum dapat memproses batch berikutnya.
    """
    print("\n--- 1. NAIVE STATIC BATCHING (Hugging Face Transformers Default) ---")
    requests = [
        {"id": "Req #1", "length": 3},  # Selesai cepat
        {"id": "Req #2", "length": 8},  # Panjang
        {"id": "Req #3", "length": 4}   # Sedang
    ]
    
    max_steps = max(r["length"] for r in requests)
    print("Mengeksekusi Batch 1 (3 Requests)...")
    for step in range(1, max_steps + 1):
        active = [r['id'] for r in requests if step <= r['length']]
        idle_gpu_slots = 3 - len(active)
        print(f"  Step {step:2d}: Active = {str(active):<24} | Slot GPU Terbuang (Idle) = {idle_gpu_slots}")
    print("⚠️ Masalah: Slot GPU menganggur (idle waste) menunggu Req #2 yang belum selesai.")

def simulate_vllm_continuous_batching():
    """
    Continuous Batching (Iteration-level Batching di vLLM):
    Ketika Req #1 selesai pada step 3, Req #4 langsung masuk pada step 4 tanpa menunggu Req #2!
    """
    print("\n--- 2. CONTINUOUS BATCHING (vLLM Engine) ---")
    
    gpu_queue = [
        {"id": "Req #1", "length": 3},
        {"id": "Req #2", "length": 6},
        {"id": "Req #3", "length": 4}
    ]
    
    incoming_pool = [
        {"id": "Req #4", "length": 5},
        {"id": "Req #5", "length": 3}
    ]
    
    gpu_slots = list(gpu_queue)
    
    for step in range(1, 9):
        # 1. kurangi sisa length
        finished = []
        for r in list(gpu_slots):
            r["length"] -= 1
            if r["length"] == 0:
                finished.append(r)
                gpu_slots.remove(r)
        
        # 2. Sisipkan request baru jika ada slot kosong
        inserted = []
        while len(gpu_slots) < 3 and incoming_pool:
            new_req = incoming_pool.pop(0)
            gpu_slots.append(new_req)
            inserted.append(new_req["id"])

        active_ids = [r["id"] for r in gpu_slots]
        fin_ids = [r["id"] for r in finished]
        ins_str = f" ➕ Inserted {inserted}" if inserted else ""
        fin_str = f" 🎉 Completed {fin_ids}" if fin_ids else ""
        print(f"  Step {step:2d}: Active = {str(active_ids):<24} |{fin_str}{ins_str}")

def explain_paged_attention():
    print("\n--- 3. MEKANISME PAGEDATTENTION (vLLM Memory Management) ---")
    print("Masalah KV Cache Tradisional: Memalokasi memori kontigu maksimum secara hipotetis -> 60-80% VRAM Terbuang!")
    print("Solusi PagedAttention      : Membagi KV Cache menjadi 'Physical Memory Blocks' non-kontigu (mirip Paging OS).")
    print("Dampak                      : Mengurangi pemborosan VRAM dari ~70% menjadi < 4%, meningkatkan Throughput 3x-4x!")

def main():
    print("=" * 75)
    print("      SIMULASI ARSITEKTUR ENGINE INFERENSI PRODUKSI (vLLM)")
    print("=" * 75)
    
    simulate_naive_batching()
    simulate_vllm_continuous_batching()
    explain_paged_attention()
    
    print("\n💡 KESIMPULAN EFFICIENCY:")
    print("• vLLM memusnahkan idle GPU time dengan Continuous Batching.")
    print("• PagedAttention memungkinkan inferensi ratusan pengguna bersamaan dalam 1 GPU.")

if __name__ == "__main__":
    main()
