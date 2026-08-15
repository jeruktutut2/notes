#!/usr/bin/env python3
"""
CLI Runner Interaktif - Context Engineering AI Learning Workspace
Berdasarkan AI Engineer Roadmap (roadmap.sh/ai-engineer)
"""

import os
import sys
import subprocess

def run_script(script_path: str):
    print(f"\n{'='*70}")
    print(f"Menjalankan: {os.path.basename(os.path.dirname(script_path))}/{os.path.basename(script_path)}")
    print(f"{'='*70}\n")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Gagal menjalankan skrip: {e}")
    except FileNotFoundError:
        print(f"\n[ERROR] File tidak ditemukan: {script_path}")
    print(f"\n{'='*70}\n")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        print("\n" + "#"*70)
        print("=== AI ENGINEERING: CONTEXT ENGINEERING LEARNING WORKSPACE ===")
        print("#"*70)
        print("Pilih modul / topik pembelajaran yang ingin Anda jalankan:\n")
        
        print("[ Modul 1: Context Window & Anatomi Context ]")
        print("  11. Context Window Architecture & Token Allocation Matrix")
        print("  12. Context Structure, Delimiters XML & Boundary Sanitization")
        print("  13. Lost in the Middle U-Shape & Streaming Attention Sinks")
        
        print("\n[ Modul 2: Context Compression & Pruning ]")
        print("  21. Selective Token Information Density Compression (LLMLingua)")
        print("  22. Semantic Truncation & Recency-Decay Sliding Window")
        print("  23. Needle In A Haystack (NIAH) Benchmark Matrix Simulator")

        print("\n[ Modul 3: In-Context Memory & State Management ]")
        print("  31. Conversation Summary Buffer & Entity Memory Store")
        print("  32. Tripartite Agent Memory (Episodic, Semantic, Procedural)")
        print("  33. Working Memory Scratchpad State Pattern")

        print("\n[ Modul 4: Dynamic Context Assembly & Caching ]")
        print("  41. Dynamic Context Assembler Pipeline & Conditional Injectors")
        print("  42. Prefix Caching & KV-Cache Latency/Cost Simulator")
        print("  43. Multi-Tenant Context Isolation & PII Redaction Sanitizer")

        print("\n[ Modul 5: Context Routing & Multi-Context Orchestration ]")
        print("  51. Hierarchical Context & Sub-Agent Context Isolation")
        print("  52. Context Sharding & Map-Reduce Pattern")

        print("\n[ Modul 6: Evaluasi, Metrik & Biaya Context ]")
        print("  61. Context Precision, Recall, Relevancy & Noise-to-Signal Ratio")
        print("  62. Context Cost Scaling, Latency TTFT & Degradation Benchmark")

        print("\n  0. Keluar")
        
        pilihan = input("\nMasukkan angka pilihan Anda (misal: 11, 21, 32, 42, 61): ").strip()
        
        scripts_map = {
            '11': "01_context_window_dan_anatomi/1_context_window_architecture_and_budgeting.py",
            '12': "01_context_window_dan_anatomi/2_context_structure_and_anatomy.py",
            '13': "01_context_window_dan_anatomi/3_loss_in_the_middle_and_attention_sinks.py",
            '21': "02_context_compression_dan_pruning/1_selective_token_compression_llmlingua.py",
            '22': "02_context_compression_dan_pruning/2_semantic_truncation_and_sliding_window.py",
            '23': "02_context_compression_dan_pruning/3_needle_in_a_haystack_niah_benchmark.py",
            '31': "03_memory_management_dan_state/1_conversation_summary_and_entity_memory.py",
            '32': "03_memory_management_dan_state/2_episodic_semantic_procedural_memory.py",
            '33': "03_memory_management_dan_state/3_working_memory_scratchpad_state.py",
            '41': "04_dynamic_context_assembly_dan_caching/1_dynamic_context_assembler_pipeline.py",
            '42': "04_dynamic_context_assembly_dan_caching/2_prefix_caching_and_kv_cache_simulator.py",
            '43': "04_dynamic_context_assembly_dan_caching/3_multi_tenant_context_hygiene_and_isolation.py",
            '51': "05_context_routing_dan_orchestration/1_hierarchical_context_and_subagent_isolation.py",
            '52': "05_context_routing_dan_orchestration/2_context_sharding_and_map_reduce.py",
            '61': "06_evaluasi_metrik_dan_biaya_context/1_context_precision_recall_relevancy.py",
            '62': "06_evaluasi_metrik_dan_biaya_context/2_context_cost_latency_degradation_benchmark.py"
        }
        
        if pilihan == '0':
            print("Keluar dari program. Selamat belajar Context Engineering!")
            break
        elif pilihan in scripts_map:
            script_path = os.path.join(base_dir, scripts_map[pilihan])
            run_script(script_path)
        else:
            print("[PERINGATAN] Pilihan tidak valid. Silakan masukkan angka yang tersedia.")

if __name__ == "__main__":
    main()
