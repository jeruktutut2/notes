"""
==============================================================================
CONTOH MODUL 4B: RAG DENGAN SENTENCE-TRANSFORMERS (LOKAL NATIVE)
==============================================================================
Versi ini menggunakan library `sentence-transformers` dari Hugging Face secara
langsung di dalam Python, alih-alih memanggil Ollama API untuk membuat embedding.
Ini berarti model embedding (misal: all-MiniLM-L6-v2) akan diunduh dan
dijalankan secara native (lokal) oleh CPU/GPU Anda.

CARA PAKAI:
    1. Pastikan Anda sudah menginstall library tambahan:
       pip install sentence-transformers torch
    2. Jalankan script:
       python main_transformer.py
==============================================================================
"""

import os
import requests
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

OLLAMA_CHAT_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
CHAT_MODEL = os.getenv("DEFAULT_MODEL", "gemma3:4b")

# Menginisialisasi model transformer secara lokal
# Saat pertama kali dijalankan, ia akan mengunduh model ~80MB dari Hugging Face
print("Memuat model sentence-transformers (all-MiniLM-L6-v2)...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

DOKUMEN_PATH = os.path.join(os.path.dirname(__file__), "documents", "contoh.txt")


# ------------------------------------------------------------------------------
# 1. FUNGSI EKSSTRAKSI EMBEDDING VIA SENTENCE-TRANSFORMERS
# ------------------------------------------------------------------------------
def dapatkan_embedding(teks: str) -> list:
    """
    Mengubah potongan teks menjadi deretan vektor float (embedding).
    Menggunakan model sentence-transformers yang berjalan secara lokal.
    """
    try:
        # .encode() mengembalikan numpy array, kita ubah ke list
        vektor = embedder.encode(teks).tolist()
        return vektor
    except Exception as e:
        print(f"❌ Error mengambil embedding: {e}")
        return []


# ------------------------------------------------------------------------------
# 2. CHUNKING TEKS (STRATEGI PEMOTONGAN DOKUMEN)
# ------------------------------------------------------------------------------
def bagi_dokumen_menjadi_chunks(filepath: str, max_lines_per_chunk: int = 5) -> list:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File dokumen tidak ditemukan di: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        konten = f.read()

    bagian_bagian = konten.split("\n\n")
    chunks = [b.strip() for b in bagian_bagian if b.strip()]
    return chunks


# ------------------------------------------------------------------------------
# 3. PIPELINE SETUP VECTOR DB (CHROMADB)
# ------------------------------------------------------------------------------
def setup_vector_database(chunks: list):
    print("\n--- [INDEXING] Menyiapkan ChromaDB Vector Database ---")
    
    chroma_client = chromadb.Client()
    koleksi = chroma_client.get_or_create_collection(name="sop_perusahaan_transformer")

    for i, chunk in enumerate(chunks):
        vektor = dapatkan_embedding(chunk)
        if vektor:
            koleksi.add(
                documents=[chunk],
                embeddings=[vektor],
                ids=[f"doc_chunk_{i+1}"]
            )
            print(f"  ✓ Indexed Chunk {i+1} ({len(vektor)} dimensi embedding transformer)")

    print("✅ Indexing Knowledge Base Selesai!")
    return koleksi


# ------------------------------------------------------------------------------
# 4. RAG QUERY PIPELINE (RETRIEVAL + GENERATION)
# ------------------------------------------------------------------------------
def tanya_rag(koleksi_chroma, pertanyaan_user: str):
    print(f"\n=========================================================")
    print(f"PERTANYAAN USER: '{pertanyaan_user}'")
    print("=========================================================")

    vektor_pertanyaan = dapatkan_embedding(pertanyaan_user)
    if not vektor_pertanyaan:
        return "❌ Gagal membuat embedding pertanyaan."

    hasil_search = koleksi_chroma.query(
        query_embeddings=[vektor_pertanyaan],
        n_results=2
    )

    chunk_terkait = hasil_search["documents"][0]
    print("\n--- [RETRIEVAL] Chunk Dokumen Relevan yang Ditemukan ---")
    for idx, c in enumerate(chunk_terkait, 1):
        print(f"[{idx}] {c[:120]}...")

    konteks_gabungan = "\n\n".join(chunk_terkait)
    
    system_prompt = f"""Kamu adalah Asisten HR AI internal perusahaan.
Jawablah pertanyaan pengguna HANYA berdasarkan KONTEKS DOKUMEN RESMI di bawah ini.
Jika informasi tidak ada dalam konteks, jawablah dengan jujur: "Maaf, informasi tidak ditemukan dalam SOP resmi kantor."

KONTEKS DOKUMEN HR PERUSAHAAN:
{konteks_gabungan}
"""

    payload = {
        "model": CHAT_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pertanyaan_user}
        ],
        "stream": False,
        "options": {"temperature": 0.1}
    }

    try:
        res = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=30)
        res.raise_for_status()
        jawaban = res.json()["message"]["content"]
        
        print("\n--- [JAWABAN LLM BERBASIS RAG] ---")
        print(jawaban)
        return jawaban
    except Exception as e:
        print(f"❌ Error RAG LLM: {e}")
        return str(e)


# ------------------------------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("=========================================================")
    print("CHATBOT INTERAKTIF: RAG (VERSI SENTENCE-TRANSFORMERS)")
    print("=========================================================")

    try:
        daftar_chunks = bagi_dokumen_menjadi_chunks(DOKUMEN_PATH)
        print(f"Dokumen berhasil dipotong menjadi {len(daftar_chunks)} chunks.")

        db_koleksi = setup_vector_database(daftar_chunks)
        
        print("\nSiap! Anda bisa mulai bertanya mengenai dokumen SOP perusahaan.")
        print("Ketik 'keluar' atau 'exit' untuk berhenti.\n")
        
        while True:
            pertanyaan = input("\nKamu: ").strip()
            if pertanyaan.lower() in ['keluar', 'exit', 'q']:
                print("Sampai jumpa!")
                break
            if not pertanyaan:
                continue
                
            tanya_rag(db_koleksi, pertanyaan)
            
    except Exception as e:
        print(f"Gagal memuat RAG sistem: {e}")
