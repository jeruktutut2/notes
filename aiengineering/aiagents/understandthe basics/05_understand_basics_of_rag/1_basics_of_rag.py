#!/usr/bin/env python3
"""
Modul 5: Understand the Basics of RAG Simulator
Simulasi end-to-end Retrieval-Augmented Generation (RAG):
Document Chunking -> Vector Embedding -> Vector Retrieval (Top-K) -> Prompt Augmentation -> LLM Synthesis.
"""

import time
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple

# ANSI Colors
HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Internal Knowledge Base Mentah (Simulasi Dokumen Perusahaan)
RAW_DOCUMENT = """
[DOKUMEN INTERNAL PERUSAHAAN TECHCORP 2026]
Kebijakan Kerja Remote dan Fasilitas Karyawan:
1. Jam Kerja Fleksibel: Seluruh karyawan dapat bekerja secara remote hingga 3 hari seminggu dengan persetujuan Lead.
2. Tunjangan Perangkat: Setiap karyawan berhak mengajukan reimbursement monitor external hingga Rp 3.500.000 setiap 2 tahun.
3. Cuti Kesehatan Mental: Perusahaan menyediakan 4 hari cuti khusus kesehatan mental di luar cuti tahunan reguler.
4. Pengajuan Klaim Medis: Klaim medis dikirimkan melalui portal HR sebelum tanggal 25 setiap bulannya.
"""

@dataclass
class DocumentChunk:
    chunk_id: int
    text: str
    vector: List[float]

def mock_embed_text(text: str) -> List[float]:
    """Mengubah teks menjadi vektor sintetis 4-dimensi berdasarkan kata kunci utama.
    [Remote/Kerja, Tunjangan/Uang, Cuti/Kesehatan, HR/Portal]
    """
    t_low = text.lower()
    v1 = 0.9 if any(k in t_low for k in ["remote", "kerja", "jam"]) else 0.05
    v2 = 0.9 if any(k in t_low for k in ["tunjangan", "perangkat", "reimbursement", "rp", "3.500.000"]) else 0.05
    v3 = 0.9 if any(k in t_low for k in ["cuti", "kesehatan", "mental", "medis"]) else 0.05
    v4 = 0.9 if any(k in t_low for k in ["hr", "portal", "klaim", "tanggal"]) else 0.05
    
    # Normalisasi vektor
    mag = math.sqrt(v1*v1 + v2*v2 + v3*v3 + v4*v4)
    return [v1/mag, v2/mag, v3/mag, v4/mag]

def cosine_sim(v1: List[float], v2: List[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2))

def chunk_document(raw_text: str) -> List[str]:
    """Memecah dokumen menjadi potongan-potongan berdasarkan baris kebijakan."""
    lines = [line.strip() for line in raw_text.strip().split("\n") if line.strip() and not line.startswith("[")]
    return lines

def run_demo():
    print(f"\n{BOLD}{HEADER}=== RETRIEVAL-AUGMENTED GENERATION (RAG) SIMULATOR ==={RESET}\n")
    
    # -------------------------------------------------------------
    # STEP 1: INGESTION & CHUNKING
    # -------------------------------------------------------------
    print(f"{BOLD}[ STEP 1: DOCUMENT INGESTION & CHUNKING ]{RESET}")
    chunks_text = chunk_document(RAW_DOCUMENT)
    vector_db: List[DocumentChunk] = []
    
    for idx, text in enumerate(chunks_text, start=1):
        vec = mock_embed_text(text)
        chunk_obj = DocumentChunk(chunk_id=idx, text=text, vector=vec)
        vector_db.append(chunk_obj)
        print(f"  • Chunk #{idx}: \"{text[:55]}...\" -> {YELLOW}Vector 4D Indexed{RESET}")

    time.sleep(0.5)

    # -------------------------------------------------------------
    # STEP 2: USER QUERY & VECTOR RETRIEVAL (TOP-K)
    # -------------------------------------------------------------
    user_query = "Berapa anggaran reimbursement monitor yang bisa diajukan karyawan?"
    print(f"\n{BOLD}[ STEP 2: USER QUERY & VECTOR SEARCH (TOP-K) ]{RESET}")
    print(f"❓ User Query: {CYAN}\"{user_query}\"{RESET}")
    
    query_vec = mock_embed_text(user_query)
    print(f"🔢 Query Vector: {query_vec}")

    # Calculate similarity score for each chunk
    scored_chunks: List[Tuple[DocumentChunk, float]] = []
    for chunk in vector_db:
        score = cosine_sim(query_vec, chunk.vector)
        scored_chunks.append((chunk, score))
        
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    
    top_k = 1  # Ambil Top-1 most relevant chunk
    retrieved_chunk, top_score = scored_chunks[0]
    
    print(f"\n{GREEN}▶ Top-{top_k} Chunk Ditemukan di Vector Store (Cosine Similarity: {top_score:.4f}):{RESET}")
    print(f"  {BOLD}\"{retrieved_chunk.text}\"{RESET}")

    time.sleep(0.5)

    # -------------------------------------------------------------
    # STEP 3: PROMPT AUGMENTATION
    # -------------------------------------------------------------
    print(f"\n{BOLD}[ STEP 3: PROMPT AUGMENTATION (CONTEXT INJECTION) ]{RESET}")
    augmented_prompt = f"""[SYSTEM INSTRUCTION]
Jawab pertanyaan pengguna HANYA berdasarkan konteks fakta yang disediakan di bawah.
Jika fakta tidak ditemukan dalam konteks, katakan bahwa informasi tidak tersedia.

[RETRIEVED CONTEXT FROM VECTOR DB]
{retrieved_chunk.text}

[USER QUESTION]
{user_query}
"""
    print(f"{YELLOW}{augmented_prompt}{RESET}")

    time.sleep(0.5)

    # -------------------------------------------------------------
    # STEP 4: LLM SYNTHESIS & HALLUCINATION COMPARISON
    # -------------------------------------------------------------
    print(f"\n{BOLD}[ STEP 4: PERBANDINGAN RESPON - DIRECT LLM VS RAG AUGMENTED ]{RESET}\n")

    print(f"{BOLD}A. Direct LLM Call (Tanpa RAG - Menjawab Tanpa Data Internal Perusahaan):{RESET}")
    print(f"  {RED}\"Sebagai model AI umum, saya tidak memiliki akses ke kebijakan internal TechCorp. Biasanya reimbursement berkisar Rp 1-2 juta bergantung perusahaan.\"{RESET}")
    print(f"  ⚠️ {RED}Respon Gagal / Halusinasi Asumsi!{RESET}\n")

    print(f"{BOLD}B. RAG-Augmented Response (Dengan Injeksi Vector Context):{RESET}")
    rag_answer = "Berdasarkan kebijakan TechCorp, setiap karyawan berhak mengajukan reimbursement monitor external hingga Rp 3.500.000 setiap 2 tahun sekali."
    print(f"  {GREEN}\"{rag_answer}\"{RESET}")
    print(f"  ✅ {GREEN}Respon 100% Akurat, Faktual, dan Bebas Halusinasi!{RESET}\n")

    print(f"{BOLD}[ KUNCI UTAMA KETANGGUHAN RAG PADA AI AGENTS ]{RESET}")
    print(" 1. Grounding Facts   : Mencegah halusinasi fakta spesifik perusahaan/domain.")
    print(" 2. Zero retraining   : Data diperbarui seketika dengan mengunggah dokumen baru ke Vector DB.")
    print(" 3. Data Privacy      : Kontrol akses dokumen sensitif dapat diatur di level Vector Store retrieval.")

if __name__ == "__main__":
    run_demo()
