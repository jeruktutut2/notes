"""
01_chunking_strategies.py
Demonstrasi Strategi Pemotongan Teks (Chunking Strategies)
- Fixed-Size Chunking (dengan Overlap)
- Sentence-Based Chunking
- Recursive Character Chunking
"""

import re
from typing import List

SAMPLE_TEXT = """
Retrieval-Augmented Generation (RAG) adalah teknik AI terkini. RAG menggabungkan Vector Database dengan LLM.
Dengan RAG, LLM dapat mengakses dokumen internal tanpa perlu fine-tuning. Hal ini mengurangi halusinasi secara signifikan.
Strategi pemotongan dokumen (chunking) sangat menentukan kualitas pencarian. Chunking yang terlalu besar menyebabkan informasi tidak relevan ikut terbawa.
Sebaliknya, chunking yang terlalu kecil menyebabkan konteks kalimat menjadi terputus-putus. Oleh karena itu, pemilihan ukuran chunk dan overlap sangat krusial.
"""

def fixed_size_chunking(text: str, chunk_size: int = 150, overlap: int = 30) -> List[str]:
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += (chunk_size - overlap)
        
    return chunks

def sentence_chunking(text: str) -> List[str]:
    # Split by sentence end punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]

def recursive_character_chunking(text: str, max_chunk_size: int = 180, separators: List[str] = None) -> List[str]:
    if separators is None:
        separators = ["\n\n", "\n", ". ", " "]
        
    def _split_text(txt: str, seps: List[str]) -> List[str]:
        if len(txt) <= max_chunk_size or not seps:
            return [txt.strip()]
        
        current_sep = seps[0]
        remaining_seps = seps[1:]
        
        parts = txt.split(current_sep)
        result = []
        current_chunk = ""
        
        for p in parts:
            candidate = current_chunk + (current_sep if current_chunk else "") + p
            if len(candidate) <= max_chunk_size:
                current_chunk = candidate
            else:
                if current_chunk:
                    result.append(current_chunk.strip())
                if len(p) > max_chunk_size and remaining_seps:
                    result.extend(_split_text(p, remaining_seps))
                    current_chunk = ""
                else:
                    current_chunk = p
        if current_chunk:
            result.append(current_chunk.strip())
        return result

    return _split_text(text, separators)

def run_chunking_demo():
    print("=" * 70)
    print("✂️ DEMONSTRASI CHUNKING STRATEGIES")
    print("=" * 70)
    
    print("\n1. 📏 Fixed-Size Chunking (Size=150, Overlap=30):")
    fixed_chunks = fixed_size_chunking(SAMPLE_TEXT, chunk_size=150, overlap=30)
    for i, c in enumerate(fixed_chunks, 1):
        print(f"   [Chunk {i}] ({len(c)} chars): \"{c}\"")
        
    print("\n2. 📝 Sentence-Based Chunking:")
    sent_chunks = sentence_chunking(SAMPLE_TEXT)
    for i, c in enumerate(sent_chunks, 1):
        print(f"   [Chunk {i}] ({len(c)} chars): \"{c}\"")
        
    print("\n3. 🔄 Recursive Character Chunking (Max Size=180):")
    rec_chunks = recursive_character_chunking(SAMPLE_TEXT, max_chunk_size=180)
    for i, c in enumerate(rec_chunks, 1):
        print(f"   [Chunk {i}] ({len(c)} chars): \"{c}\"")
        
    print("=" * 70)

if __name__ == "__main__":
    run_chunking_demo()
