"""
Modul 06: Merging, Export & Inference
Skrip 2: Testing Inference Model Fine-Tuned (Greedy vs Sampling, Temperature & Top-P)
"""

import numpy as np

def simulate_temperature_top_p_sampling(logits, temperature=0.7, top_p=0.9):
    """
    Simulasi logika penyesuaian logits berdasarkan Temperature dan Top-P (Nucleus Sampling).
    """
    # 1. Aplikasi Temperature: logits / T
    scaled_logits = logits / max(temperature, 1e-5)
    
    # 2. Softmax ke Probabilitas
    exp_logits = np.exp(scaled_logits - np.max(scaled_logits))
    probs = exp_logits / np.sum(exp_logits)
    
    # 3. Sort probabilitas terbalik
    sorted_indices = np.argsort(probs)[::-1]
    sorted_probs = probs[sorted_indices]
    
    # 4. Top-P (Nucleus) Cutoff
    cumulative_probs = np.cumsum(sorted_probs)
    cutoff_index = np.searchsorted(cumulative_probs, top_p) + 1
    
    selected_indices = sorted_indices[:cutoff_index]
    selected_probs = sorted_probs[:cutoff_index]
    selected_probs /= np.sum(selected_probs) # Renormalisasi
    
    # Sample 1 token index
    sampled_idx = np.random.choice(selected_indices, p=selected_probs)
    return sampled_idx

def demo_inference_decoding():
    print("=" * 60)
    print("MODUL 06 - SKRIP 2: Inference & Decoding Strategies")
    print("=" * 60)
    
    vocab = ["LoRA", "SFT", "Quantization", "Transformer", "RAG", "Prompt", "Gradient", "Loss"]
    mock_logits = np.array([4.2, 3.8, 2.1, 1.5, 0.8, 0.5, -0.2, -1.0])
    
    print("\n--- 1. Greedy Search Decoding (Temperature = 0.0) ---")
    greedy_idx = np.argmax(mock_logits)
    print(f"Top-1 Token Terpilih (Deterministik): '{vocab[greedy_idx]}'")
    
    print("\n--- 2. Nucleus Sampling (Temperature = 0.7, Top-P = 0.9) ---")
    np.random.seed(42)
    sampled_idx = simulate_temperature_top_p_sampling(mock_logits, temperature=0.7, top_p=0.9)
    print(f"Token Terpilih via Nucleus Sampling : '{vocab[sampled_idx]}'")
    
    print("\n--- 3. Panduan Pengaturan Parameter Inference ---")
    print("- **Kreativitas / Penulisan Bebas:** Temperature = 0.7 - 0.8, Top-P = 0.9")
    print("- **Ekstraksi Data / Coding / Matkul:** Temperature = 0.0 - 0.2 (Greedy Search agar konsisten)")
    print("- **System Prompt Compliance:** Selalu sertakan system prompt persis seperti saat fase Fine-Tuning!")

if __name__ == "__main__":
    demo_inference_decoding()
