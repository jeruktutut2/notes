"""
Modul 01: Persiapan Dataset & Formatting
Skrip 3: Tokenization & Chat Templates dengan Target-Only Loss Masking
"""

def simulate_chatml_formatting(system_prompt, user_msg, assistant_msg):
    """
    Format string mentah dengan penanda ChatML (<|im_start|>, <|im_end|>).
    """
    prompt_part = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_msg}<|im_end|>\n<|im_start|>assistant\n"
    response_part = f"{assistant_msg}<|im_end|>"
    full_text = prompt_part + response_part
    return prompt_part, response_part, full_text

def simulate_target_loss_masking(prompt_tokens, response_tokens):
    """
    Mengubah label token prompt menjadi -100 agar loss hanya dihitung pada token respon.
    """
    full_input_ids = prompt_tokens + response_tokens
    # Masking prompt dengan -100
    labels = [-100] * len(prompt_tokens) + response_tokens
    return full_input_ids, labels

def demo_tokenization():
    print("=" * 60)
    print("MODUL 01 - SKRIP 3: Tokenization & Target Loss Masking")
    print("=" * 60)
    
    system_prompt = "Anda adalah AI Assistant bidang Fine-Tuning."
    user_msg = "Bagaimana cara melakukan masking pada loss?"
    assistant_msg = "Gunakan label -100 pada token prompt pengguna."
    
    prompt_str, resp_str, full_str = simulate_chatml_formatting(system_prompt, user_msg, assistant_msg)
    
    print("\n--- 1. Hasil Format String ChatML ---")
    print(full_str)
    
    # Simulasikan ID Token dummy
    mock_prompt_tokens = [101, 2045, 1000, 3050, 102]
    mock_resp_tokens = [4001, 5012, 1000, 9999, 103]
    
    full_ids, labels = simulate_target_loss_masking(mock_prompt_tokens, mock_resp_tokens)
    
    print("\n--- 2. Input IDs vs Labels (Target-Only Loss) ---")
    print(f"Full Input IDs: {full_ids}")
    print(f"Target Labels : {labels}")
    print("\nPenjelasan:")
    print("- Token bernilai -100 pada label akan diabaikan oleh PyTorch CrossEntropyLoss.")
    print("- Hal ini memastikan model melatih kemampuan menghasilkan jawaban, bukan menghafal prompt soal!")

if __name__ == "__main__":
    demo_tokenization()
