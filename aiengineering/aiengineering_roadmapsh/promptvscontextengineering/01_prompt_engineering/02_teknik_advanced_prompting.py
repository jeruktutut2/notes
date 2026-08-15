#!/usr/bin/env python3
"""
Modul 01: Teknik Advanced Prompting
Membahas Zero-Shot, Few-Shot, Chain-of-Thought (CoT), Self-Consistency Voting, Tree-of-Thought (ToT), dan ReAct.
"""

import json
import math
from typing import List, Dict, Any

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def print_header(title: str):
    print("\n" + "=" * 70)
    print(color(f"  {title}", "1;34"))
    print("=" * 70)

class AdvancedPromptingSimulator:
    """Simulasi Teknik Prompting Lanjutan"""

    @staticmethod
    def zero_shot_vs_few_shot(text: str) -> Dict[str, Any]:
        """Simulasi klasifikasi sentimen dengan Zero-shot vs Few-shot"""
        zero_shot_prompt = f"Klasifikasikan sentimen kalimat ini ke [POSITIF, NEGATIF, NETRAL]: '{text}'"
        few_shot_prompt = f"""Klasifikasikan sentimen teks berikut dengan mengikuti contoh:

Teks: 'Layanan sangat cepat dan ramah!' => Sentimen: POSITIF
Teks: 'Aplikasi sering crash saat pembayaran' => Sentimen: NEGATIF
Teks: 'Paket tiba sesuai jadwal hari ini' => Sentimen: NETRAL

Teks: '{text}' => Sentimen:"""

        return {
            "input_text": text,
            "zero_shot": {
                "prompt_tokens": 18,
                "confidence": 0.72,
                "result": "NEGATIF"
            },
            "few_shot": {
                "prompt_tokens": 65,
                "confidence": 0.96,
                "result": "NEGATIF",
                "reason": "Mengikuti pola struktur contoh eksplisit"
            }
        }

    @staticmethod
    def chain_of_thought_cot(problem: str) -> Dict[str, Any]:
        """Simulasi Chain-of-Thought (CoT) Reasoning"""
        standard_prompt = f"Soal: {problem}\nBerapa hasilnya?"
        cot_prompt = f"Soal: {problem}\nMari kita selesaikan langkah demi langkah (Step-by-step reasoning):"

        reasoning_steps = [
            "Langkah 1: Identifikasi jumlah awal apel = 15 buah.",
            "Langkah 2: Toko menjual 5 apel kepada Budi -> sisa = 15 - 5 = 10 buah.",
            "Langkah 3: Toko menerima pasokan 12 apel baru -> total = 10 + 12 = 22 buah.",
            "Langkah 4: 2 apel busuk dan dibuang -> sisa akhir = 22 - 2 = 20 buah."
        ]
        
        return {
            "problem": problem,
            "standard_prompt_result": {"answer": "22 (Salah - lupa menghitung apel busuk)", "accuracy": "Low"},
            "cot_prompt_result": {
                "reasoning_steps": reasoning_steps,
                "final_answer": "20 buah apel",
                "accuracy": "High (100%)"
            }
        }

    @staticmethod
    def self_consistency_voting(problem: str, num_samples: int = 5) -> Dict[str, Any]:
        """Simulasi Self-Consistency (Majority Voting dari multiple CoT paths)"""
        generated_paths = [
            {"path": 1, "reasoning": "15 - 5 + 12 - 2 = 20", "answer": 20},
            {"path": 2, "reasoning": "15 - 5 = 10; 10 + 12 = 22; 22 - 2 = 20", "answer": 20},
            {"path": 3, "reasoning": "15 + 12 - 5 = 22; 22 - 2 = 20", "answer": 20},
            {"path": 4, "reasoning": "15 - 5 + 12 = 22 (lupa apel busuk)", "answer": 22},
            {"path": 5, "reasoning": "15 - 5 = 10; 10 + 12 - 2 = 20", "answer": 20},
        ]
        
        # Majority voting calculation
        votes = {}
        for p in generated_paths:
            ans = p["answer"]
            votes[ans] = votes.get(ans, 0) + 1
            
        winning_answer = max(votes, key=votes.get)
        confidence = votes[winning_answer] / len(generated_paths)

        return {
            "problem": problem,
            "paths_sampled": generated_paths,
            "vote_tally": votes,
            "majority_answer": winning_answer,
            "confidence_score": f"{confidence * 100:.1f}%"
        }

    @staticmethod
    def react_framework_demo(query: str) -> List[Dict[str, str]]:
        """Simulasi ReAct (Reasoning + Acting + Observation Loop)"""
        trajectory = [
            {
                "thought_1": "Pengguna bertanya tentang cuaca Jakarta hari ini dan rekomendasi pakaian.",
                "action_1": "search_weather(city='Jakarta')",
                "observation_1": "Suhu: 32°C, Cuaca: Cerah Berawan, Kelembapan: 75%"
            },
            {
                "thought_2": "Suhu 32°C cukup panas. Saya perlu memeriksa indeks UV untuk saran pakaian.",
                "action_2": "get_uv_index(city='Jakarta')",
                "observation_2": "UV Index: 9 (Sangat Tinggi - Sangat Terik)"
            },
            {
                "thought_3": "Informasi lengkap. Saya dapat menyusun jawaban akhir dengan saran pakaian kasual ringan dan tabur surya.",
                "final_answer": "Suhu Jakarta saat ini 32°C dengan UV Index 9 (Sangat Tinggi). Disarankan mengenakan pakaian katun tipis berwarna cerah, membawa kacamata hitam, dan memakai sunscreen SPF 30+."
            }
        ]
        return trajectory

def main():
    print_header("MODUL 01: TEKNIK ADVANCED PROMPTING")
    
    # 1. Few-Shot Demonstration
    print(color("\n1. Zero-Shot vs Few-Shot Prompting:", "1;33"))
    sample_text = "Aplikasi ini memotong saldo saya dua kali padahal transaksi gagal!"
    res_shot = AdvancedPromptingSimulator.zero_shot_vs_few_shot(sample_text)
    print(f"Input Teks : '{sample_text}'")
    print(color(f"Zero-Shot  : Confidence {res_shot['zero_shot']['confidence']} | Output: {res_shot['zero_shot']['result']}", "31"))
    print(color(f"Few-Shot   : Confidence {res_shot['few_shot']['confidence']} | Output: {res_shot['few_shot']['result']} ({res_shot['few_shot']['reason']})", "32"))

    # 2. Chain-of-Thought
    print(color("\n2. Chain-of-Thought (CoT) Reasoning:", "1;33"))
    math_problem = "Toko A memiliki 15 apel. Menjual 5 ke Budi, menerima 12 dari supplier, lalu 2 busuk dibuang. Berapa apel sisa?"
    res_cot = AdvancedPromptingSimulator.chain_of_thought_cot(math_problem)
    print(f"Soal: {math_problem}")
    print(color(f"Standard Prompt Output : {res_cot['standard_prompt_result']['answer']}", "31"))
    print(color("CoT Reasoning Steps    :", "32"))
    for step in res_cot['cot_prompt_result']['reasoning_steps']:
        print(f"   • {step}")
    print(color(f"Hasil Akhir CoT        : {res_cot['cot_prompt_result']['final_answer']}", "1;32"))

    # 3. Self-Consistency Voting
    print(color("\n3. Self-Consistency (Majority Voting):", "1;33"))
    res_sc = AdvancedPromptingSimulator.self_consistency_voting(math_problem)
    print(f"Hasil Voting dari {len(res_sc['paths_sampled'])} Jalur Penalaran:")
    print(f"   Tally Suara : {res_sc['vote_tally']}")
    print(color(f"   Jawaban Mayoritas: {res_sc['majority_answer']} (Tingkat Keyakinan: {res_sc['confidence_score']})", "1;36"))

    # 4. ReAct Framework
    print(color("\n4. ReAct (Thought -> Action -> Observation):", "1;33"))
    query = "Bagaimana cuaca Jakarta dan apa pakaian yang cocok?"
    trajectory = AdvancedPromptingSimulator.react_framework_demo(query)
    print(f"Query: '{query}'")
    for idx, step in enumerate(trajectory, 1):
        if "final_answer" in step:
            print(color(f"\n   [Step {idx} - Jawaban Akhir]", "1;32"))
            print(f"   Thought : {step['thought_3']}")
            print(color(f"   Response: {step['final_answer']}", "1;32"))
        else:
            print(color(f"\n   [Step {idx} - Loop ReAct]", "35"))
            print(f"   Thought     : {step[f'thought_{idx}']}")
            print(f"   Action      : {step[f'action_{idx}']}")
            print(f"   Observation : {step[f'observation_{idx}']}")

    print_header("RANGKUMAN TEKNIK PROMPTING ADVANCED")
    print("✓ Few-Shot memberikan pola in-context yang meningkatkan akurasi format dan klasifikasi.")
    print("✓ CoT mendobrak kompleksitas penalaran matematika dan logika menjadi instruksi sekuensial.")
    print("✓ Self-Consistency mengeksekusi multiple CoT dan mengambil modus statistik untuk konsistensi.")
    print("✓ ReAct menggabungkan penalaran LLM dengan alat eksternal (APIs/Search) secara dinamis.")

if __name__ == "__main__":
    main()
