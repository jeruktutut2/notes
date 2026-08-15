"""
05_generation_synthesis.py
Sintesis Jawaban LLM Berbasis Konteks yang Diambil (Prompt Generation & Grounding)
"""

from typing import List, Dict

SYSTEM_PROMPT_TEMPLATE = """
Anda adalah asisten kecerdasan buatan (AI) yang profesional, jujur, dan presisi.
Tugas Anda adalah menjawab pertanyaan pengguna HANYA berdasarkan konteks dokumen yang disediakan di bawah ini.

ATURAN KETAT:
1. Jangan membuat asumsi atau menggunakan pengetahuan eksternal di luar konteks.
2. Jika jawaban tidak ditemukan secara tersurat dalam konteks, katakan: "Maaf, informasi tidak tersedia dalam dokumen internal kami."
3. Sertakan nomor ID dokumen atau sitasi sumber di akhir jawaban.

--- KONTEKS DOKUMEN ---
{retrieved_context}
-----------------------
"""

def generate_augmented_prompt(query: str, retrieved_chunks: List[Dict[str, str]]) -> str:
    formatted_context = ""
    for idx, chunk in enumerate(retrieved_chunks, 1):
        formatted_context += f"[{chunk['id']}] {chunk['text']}\n"
        
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(retrieved_context=formatted_context.strip())
    full_prompt = f"{system_prompt}\nPERTANYAAN PENGGUNA:\n{query}\n\nJAWABAN AI (DISERTAI SITASI):"
    return full_prompt

def mock_llm_response(query: str, retrieved_chunks: List[Dict[str, str]]) -> str:
    prompt = generate_augmented_prompt(query, retrieved_chunks)
    
    # Mock generation logic for demonstration
    if "garansi" in query.lower():
        return "Laptop Gaming ASUS ROG dilengkapi garansi resmi selama 2 tahun di Service Center resmi. [Sumber: Dokumen #1]"
    else:
        return "Maaf, informasi tidak tersedia dalam dokumen internal kami."

def run_generation_demo():
    print("=" * 70)
    print("🤖 DEMONSTRASI GENERATION & CONTEXT SYNTHESIS")
    print("=" * 70)
    
    retrieved_chunks = [
        {"id": "DOC-101", "text": "Laptop Gaming ASUS ROG memiliki garansi resmi 2 tahun di Service Center resmi."},
        {"id": "DOC-102", "text": "Layanan klaim garansi memerlukan nota pembelian asli dan kartu garansi."}
    ]
    
    query = "Berapa lama garansi Laptop Gaming ASUS ROG dan apa syaratnya?"
    
    print("📝 Augmented System Prompt Yang Dikirim ke LLM:")
    print("-" * 50)
    prompt = generate_augmented_prompt(query, retrieved_chunks)
    print(prompt)
    print("-" * 50)
    
    print("\n💬 Jawaban Sintesis LLM:")
    response = mock_llm_response(query, retrieved_chunks)
    print(f"   {response}")
    print("=" * 70)

if __name__ == "__main__":
    run_generation_demo()
