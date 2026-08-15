#!/usr/bin/env python3
"""
Modul 02: Arsitektur Model Transformer
Simulasi dan penjelasan visual mengenai 3 jenis arsitektur Transformer:
1. Encoder-Only (BERT / Embeddings)
2. Decoder-Only (GPT / Autoregressive LLM)
3. Encoder-Decoder (T5 / Sequence-to-Sequence)
"""

def print_header(title: str):
    print("\n" + "=" * 70)
    print(f"  {title.upper()}")
    print("=" * 70)

def simulate_encoder_only(text: str):
    """
    Encoder-Only (Bi-directional Attention):
    Melihat seluruh konteks kalimat secara bersamaan untuk menghasilkan Vector Embedding.
    """
    print(f"\n[ENCODER-ONLY: BERT / EMBEDDINGS]")
    print(f"Input Text: '{text}'")
    print("Attention Pattern: Full Bi-Directional (Token A memperhatikan Token B & C simultan)")
    
    # Mocking vector embedding output 4-dimensi untuk visualisasi
    tokens = text.split()
    print("\nVector Representation (Embeddings per Token):")
    for i, token in enumerate(tokens):
        mock_vector = [round((i + 1) * 0.123 + j * 0.05, 3) for j in range(4)]
        print(f"  Token '{token:10s}' -> Vector: {mock_vector}")
    print("Primary Use Cases: Semantic Search, Vector DB Indexing, Sentiment Classification.")

def simulate_decoder_only(prompt: str, max_tokens: int = 5):
    """
    Decoder-Only (Causal Autoregressive Attention):
    Melihat token sebelumnya saja (Causal Masking) untuk memprediksi token berikutnya satu-per-satu.
    """
    print(f"\n[DECODER-ONLY: GPT / LLAMA / MISTRAL]")
    print(f"Initial Prompt: '{prompt}'")
    print("Attention Pattern: Causal Masked (Token N hanya melihat token 1..N-1)")
    
    generated_tokens = ["adalah", "bidang", "teknologi", "yang", "pesat."]
    current_text = prompt
    
    print("\nAutoregressive Next Token Generation Steps:")
    for step in range(min(max_tokens, len(generated_tokens))):
        next_tok = generated_tokens[step]
        print(f"  Step {step + 1}: Context = '{current_text}' ---> Predicted Next Token = '{next_tok}'")
        current_text += " " + next_tok
    
    print(f"\nFinal Result: '{current_text}'")
    print("Primary Use Cases: Generative Chat, Code Generation, Reasoning & Agentic Workflows.")

def simulate_encoder_decoder(input_text: str):
    """
    Encoder-Decoder (Cross-Attention):
    Encoder memproses input lengkap, Decoder menghasilkan output urut berdasarkan hasil Encoder.
    """
    print(f"\n[ENCODER-DECODER: T5 / BART / WHISPER]")
    print(f"Source Input (English): '{input_text}'")
    print("1. Encoder Phase: Converting full source input to Latent Context Matrix...")
    print("2. Decoder Phase: Generating Target Output via Cross-Attention...")
    
    translated = "Kecerdasan Buatan mengubah dunia."
    print(f"Target Output (Indonesian Translation): '{translated}'")
    print("Primary Use Cases: Machine Translation, Text Summarization, Audio Transcription.")

def main():
    print_header("Arsitektur Utama Transformer (Vaswani et al., 2017)")
    
    sample_text = "AI Engineering"
    
    simulate_encoder_only("Belajar AI Engineering sangat menyenangkan")
    simulate_decoder_only("AI Engineering", max_tokens=4)
    simulate_encoder_decoder("Artificial Intelligence changes the world")
    
    print_header("Ringkasan Matriks Arsitektur")
    print(f"{'Arsitektur':<18} | {'Attention Type':<20} | {'Output':<18} | {'Contoh Model'}")
    print("-" * 75)
    print(f"{'Encoder-Only':<18} | {'Bi-directional':<20} | {'Vector Embeddings':<18} | BERT, RoBERTa")
    print(f"{'Decoder-Only':<18} | {'Causal Masked':<20} | {'Autoregressive Text':<18} | GPT-4, Llama 3, Qwen")
    print(f"{'Encoder-Decoder':<18} | {'Cross-Attention':<20} | {'Seq-to-Seq Text':<18} | T5, BART, Whisper")

if __name__ == "__main__":
    main()
