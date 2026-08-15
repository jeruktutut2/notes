#!/usr/bin/env python3
"""
Modul 03: Zero-Shot vs Few-Shot & Role Prompting Demo
Demonstrasi perbandingan Zero-shot, Few-shot, dan Role Prompting.
"""

def demo_zero_vs_few_shot():
    print("🎯 DEMO: ZERO-SHOT VS FEW-SHOT PROMPTING")
    print("=" * 60)
    
    task_input = "Produk laptop ini baterainya tahan 15 jam tapi kipasnya sangat bising."
    
    # 1. Zero-Shot Prompt
    zero_shot_prompt = f"""
    Ekstrak entitas dan sentimen dari ulasan berikut:
    "{task_input}"
    """
    
    # 2. Few-Shot Prompt
    few_shot_prompt = f"""
    Ekstrak entitas dan sentimen produk ke dalam format JSON.
    
    Contoh 1:
    Input: "Layar HP ini sangat jernih tetapi chargernya lambat."
    Output: {{"Layar": "Positif", "Charger": "Negatif"}}
    
    Contoh 2:
    Input: "Kamera bagus, bodi kokoh, harga terjangkau."
    Output: {{"Kamera": "Positif", "Bodi": "Positif", "Harga": "Positif"}}
    
    Input: "{task_input}"
    Output:
    """
    
    print("--- [ZERO-SHOT PROMPT] ---")
    print(zero_shot_prompt.strip())
    
    print("\n--- [FEW-SHOT PROMPT (IN-CONTEXT LEARNING)] ---")
    print(few_shot_prompt.strip())
    print("=" * 60)

if __name__ == "__main__":
    demo_zero_vs_few_shot()
