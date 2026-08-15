"""
==============================================================================
CONTOH MODUL 4: RAG (RETRIEVAL-AUGMENTED GENERATION)
==============================================================================
RAG memungkinkan AI menjawab pertanyaan tentang dokumen internal perusahaan
yang TIDAK PERNAH dipelajari saat proses training awal LLM.

ALUR RAG END-TO-END:
    FASE INDEXING (Setup Knowledge Base):
        1. Baca dokumen fisik (.txt)
        2. Chunking (Memotong teks menjadi paragraf kecil)
        3. Embedding (Mengubah teks potongan menjadi Vektor Angka via nomic-embed-text)
        4. Menyimpan Vektor ke Vector Database (ChromaDB)

    FASE QUERY (Tanya Jawab):
        5. User bertanya -> Konversi pertanyaan ke Vektor Embedding
        6. Cari Chunk dokumen paling mirip secara makna di ChromaDB
        7. Augmentasi: Gabungkan chunk relevan ke dalam Context Prompt LLM
        8. Generasi: LLM menjawab pertanyaan HANYA berdasarkan konteks dokumen.

CARA PAKAI:
    1. Pastikan model embedding terpasang: ollama pull nomic-embed-text
    2. Pastikan model chat terpasang:      ollama pull gemma3:4b
    3. Jalankan script:                    python main.py
==============================================================================
"""

import os
import requests
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()

OLLAMA_CHAT_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_EMBED_URL = os.getenv("OLLAMA_EMBED_URL", "http://localhost:11434/api/embeddings")
CHAT_MODEL = os.getenv("DEFAULT_MODEL", "gemma3:4b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

DOKUMEN_PATH = os.path.join(os.path.dirname(__file__), "documents", "contoh.txt")


# ------------------------------------------------------------------------------
# 1. FUNGSI EKSSTRAKSI EMBEDDING VIA OLLAMA
# ------------------------------------------------------------------------------
def dapatkan_embedding(teks: str) -> list:
    """
    Mengubah potongan teks menjadi deretan vektor float (embedding).
    Menggunakan model nomic-embed-text via Ollama API.
    """
    payload = {
        "model": EMBED_MODEL,
        "prompt": teks
    }
    try:
        response = requests.post(OLLAMA_EMBED_URL, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["embedding"]
    except Exception as e:
        print(f"❌ Error mengambil embedding: {e}")
        return []


# ------------------------------------------------------------------------------
# 2. CHUNKING TEKS (STRATEGI PEMOTONGAN DOKUMEN)
# ------------------------------------------------------------------------------
def bagi_dokumen_menjadi_chunks(filepath: str, max_lines_per_chunk: int = 5) -> list:
    """
    Membaca dokumen teks dan memotongnya menjadi chunk paragraf kecil.
    Chunking penting agar pencarian vektor lebih fokus dan presisi.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File dokumen tidak ditemukan di: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        konten = f.read()

    # Memisah berdasarkan paragraf atau section
    bagian_bagian = konten.split("\n\n")
    chunks = [b.strip() for b in bagian_bagian if b.strip()]
    return chunks


# ------------------------------------------------------------------------------
# 3. PIPELINE SETUP VECTOR DB (CHROMADB)
# ------------------------------------------------------------------------------
def setup_vector_database(chunks: list):
    """
    Inisialisasi ChromaDB lokal dan memasukkan chunk dokumen beserta vektor embedding-nya.
    """
    print("\n--- [INDEXING] Menyiapkan ChromaDB Vector Database ---")
    
    # Inisialisasi client ChromaDB in-memory (dapat diubah ke persistent di disk)
    chroma_client = chromadb.Client()
    
    # Buat atau ambil koleksi vector store
    koleksi = chroma_client.get_or_create_collection(name="sop_perusahaan")

    # Loop setiap chunk dan hitung embeddingnya
    for i, chunk in enumerate(chunks):
        vektor = dapatkan_embedding(chunk)
        if vektor:
            koleksi.add(
                documents=[chunk],
                embeddings=[vektor],
                ids=[f"doc_chunk_{i+1}"]
            )
            print(f"  ✓ Indexed Chunk {i+1} ({len(vektor)} dimensi embedding)")

    print("✅ Indexing Knowledge Base Selesai!")
    return koleksi


# ------------------------------------------------------------------------------
# 4. RAG QUERY PIPELINE (RETRIEVAL + GENERATION)
# ------------------------------------------------------------------------------
def tanya_rag(koleksi_chroma, pertanyaan_user: str):
    """
    Eksekusi alur RAG: Mencari chunk relevan di ChromaDB lalu mengirimnya ke LLM.
    """
    print(f"\n=========================================================")
    print(f"PERTANYAAN USER: '{pertanyaan_user}'")
    print("=========================================================")

    # 1. Konversi pertanyaan pengguna ke Vektor Embedding
    vektor_pertanyaan = dapatkan_embedding(pertanyaan_user)
    if not vektor_pertanyaan:
        return "❌ Gagal membuat embedding pertanyaan."

    # 2. Search ke ChromaDB (Cari Top 2 chunk paling mirip secara makna)
    hasil_search = koleksi_chroma.query(
        query_embeddings=[vektor_pertanyaan],
        n_results=2
    )
    print(f"hasil_search: {hasil_search}")

    chunk_terkait = hasil_search["documents"][0]
    print("\n--- [RETRIEVAL] Chunk Dokumen Relevan yang Ditemukan ---")
    for idx, c in enumerate(chunk_terkait, 1):
        print(f"[{idx}] {c[:120]}...")

    # 3. Augmentasi Konteks ke Prompt LLM
    konteks_gabungan = "\n\n".join(chunk_terkait)
    
    system_prompt = f"""Kamu adalah Asisten HR AI internal perusahaan.
Jawablah pertanyaan pengguna HANYA berdasarkan KONTEKS DOKUMEN RESMI di bawah ini.
Jika informasi tidak ada dalam konteks, jawablah dengan jujur: "Maaf, informasi tidak ditemukan dalam SOP resmi kantor."

KONTEKS DOKUMEN HR PERUSAHAAN:
{konteks_gabungan}
"""

    # 4. Generasi Jawaban oleh LLM
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
    print("CHATBOT INTERAKTIF: RAG SYSTEM (MODUL 4)")
    print("=========================================================")

    try:
        # 1. Chunking Dokumen
        daftar_chunks = bagi_dokumen_menjadi_chunks(DOKUMEN_PATH)
        print(f"Dokumen berhasil dipotong menjadi {len(daftar_chunks)} chunks.")

        # 2. Indexing ke Vector DB
        db_koleksi = setup_vector_database(daftar_chunks)
        
        print("\nSiap! Anda bisa mulai bertanya mengenai dokumen SOP perusahaan.")
        print("Ketik 'keluar' atau 'exit' untuk berhenti.\n")
        
        # 3. Uji Coba Tanya Jawab RAG (Interactive Loop)
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
