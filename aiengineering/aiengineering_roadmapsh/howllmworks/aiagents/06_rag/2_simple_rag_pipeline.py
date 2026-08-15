import os
import numpy as np
from openai import OpenAI

def main():
    print("=== 6.2 Simple RAG Pipeline ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # ---------------------------------------------------------------
    # RAG (Retrieval-Augmented Generation)
    # Alur: Query → RETRIEVE dokumen relevan → AUGMENT prompt → GENERATE jawaban
    #
    # Masalah yang dipecahkan RAG:
    # - LLM tidak tahu data internal perusahaan
    # - LLM bisa outdated (training data punya cutoff date)
    # - LLM bisa halusinasi (mengarang fakta)
    #
    # Solusi: Cari dokumen relevan dulu, lalu masukkan ke prompt
    # sebagai konteks agar LLM menjawab berdasarkan FAKTA.
    # ---------------------------------------------------------------

    # --- KNOWLEDGE BASE (sumber pengetahuan) ---
    # Simulasi dokumen internal perusahaan
    knowledge_base = [
        {
            "id": 1,
            "judul": "Kebijakan Cuti",
            "konten": "Karyawan berhak atas 12 hari cuti tahunan. Cuti bisa diambil setelah masa percobaan 3 bulan. Cuti yang tidak digunakan bisa diakumulasi maksimal 5 hari ke tahun berikutnya. Pengajuan cuti minimal 3 hari kerja sebelumnya melalui sistem HR."
        },
        {
            "id": 2,
            "judul": "Jam Kerja",
            "konten": "Jam kerja normal adalah Senin-Jumat, 09:00-18:00 WIB dengan istirahat 1 jam. Kebijakan WFH berlaku 2 hari per minggu (Selasa dan Kamis). Lembur harus disetujui oleh atasan dan dikompensasi 1.5x upah per jam."
        },
        {
            "id": 3,
            "judul": "Benefit Karyawan",
            "konten": "Benefit meliputi: BPJS Kesehatan dan Ketenagakerjaan, asuransi kesehatan swasta (termasuk keluarga inti), tunjangan makan Rp 35.000/hari, tunjangan transport Rp 500.000/bulan, dan akses ke gym kantor."
        },
        {
            "id": 4,
            "judul": "Proses Rekrutmen",
            "konten": "Proses rekrutmen terdiri dari: screening CV, tes teknis online, interview HR, interview user/manager, dan offering. Total proses biasanya 2-3 minggu. Referral bonus Rp 5.000.000 jika kandidat lulus masa percobaan."
        },
        {
            "id": 5,
            "judul": "IT Support",
            "konten": "Untuk masalah IT, hubungi helpdesk di ext. 100 atau email it-support@perusahaan.com. Password reset bisa dilakukan mandiri melalui portal SSO. Laptop baru bisa diajukan setelah 3 tahun pemakaian."
        }
    ]

    # --- SIMPLE RETRIEVER (menggunakan pseudo-embedding) ---
    def pseudo_embedding(text, dim=64):
        np.random.seed(hash(text.lower().strip()) % (2**31))
        vec = np.random.randn(dim).astype(np.float32)
        return vec / (np.linalg.norm(vec) + 1e-8)

    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

    # Index semua dokumen
    doc_embeddings = []
    for doc in knowledge_base:
        emb = pseudo_embedding(doc["judul"] + " " + doc["konten"])
        doc_embeddings.append(emb)

    def retrieve(query, top_k=2):
        """RETRIEVE: Cari dokumen paling relevan."""
        query_emb = pseudo_embedding(query)
        similarities = []
        for i, doc_emb in enumerate(doc_embeddings):
            sim = cosine_similarity(query_emb, doc_emb)
            similarities.append((i, sim))
        similarities.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, sim in similarities[:top_k]:
            results.append({
                "dokumen": knowledge_base[idx],
                "similarity": sim
            })
        return results

    # --- RAG PIPELINE ---
    def rag_pipeline(pertanyaan):
        """Pipeline RAG lengkap: Retrieve → Augment → Generate."""
        print(f"\n{'='*60}")
        print(f"❓ Pertanyaan: {pertanyaan}")
        print(f"{'='*60}")

        # STEP 1: RETRIEVE
        print("\n📚 [RETRIEVE] Mencari dokumen relevan...")
        retrieved_docs = retrieve(pertanyaan, top_k=2)

        context = ""
        for i, r in enumerate(retrieved_docs):
            doc = r["dokumen"]
            print(f"   [{i+1}] (sim={r['similarity']:.3f}) {doc['judul']}")
            context += f"\n--- Dokumen: {doc['judul']} ---\n{doc['konten']}\n"

        # STEP 2: AUGMENT
        print("\n📝 [AUGMENT] Menyusun prompt dengan konteks...")
        augmented_prompt = f"""Berdasarkan dokumen internal perusahaan berikut:

{context}

Jawab pertanyaan karyawan berikut dengan akurat berdasarkan dokumen di atas.
Jika informasi tidak ada di dokumen, katakan bahwa kamu tidak memiliki informasinya.

Pertanyaan: {pertanyaan}"""

        print(f"   Panjang prompt: {len(augmented_prompt)} karakter")

        # STEP 3: GENERATE
        print("\n🤖 [GENERATE] Meminta LLM menjawab...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Kamu adalah asisten HR perusahaan. Jawab berdasarkan dokumen yang diberikan, dalam Bahasa Indonesia."
                },
                {"role": "user", "content": augmented_prompt}
            ],
            temperature=0.2
        )

        jawaban = response.choices[0].message.content
        print(f"\n💬 Jawaban:\n{jawaban}")

        return jawaban

    # --- DEMO ---
    print("=" * 60)
    print("DEMO: RAG Pipeline untuk Asisten HR")
    print("=" * 60)

    pertanyaan_list = [
        "Berapa hari cuti yang saya dapatkan per tahun?",
        "Bagaimana kebijakan WFH di perusahaan?",
        "Apa saja benefit yang saya dapat sebagai karyawan?",
        "Bagaimana cara reset password?",
    ]

    for pertanyaan in pertanyaan_list:
        rag_pipeline(pertanyaan)

    # Perbandingan: TANPA RAG vs DENGAN RAG
    print(f"\n{'='*60}")
    print("PERBANDINGAN: Tanpa RAG vs Dengan RAG")
    print(f"{'='*60}")

    test_q = "Berapa tunjangan makan per hari di perusahaan?"
    print(f"\nPertanyaan: {test_q}\n")

    # Tanpa RAG
    print("--- TANPA RAG (LLM menjawab dari pengetahuan umum) ---")
    response_no_rag = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Kamu adalah asisten HR. Jawab dalam Bahasa Indonesia."},
            {"role": "user", "content": test_q}
        ],
        temperature=0.2
    )
    print(f"Jawaban: {response_no_rag.choices[0].message.content}\n")

    # Dengan RAG
    print("--- DENGAN RAG (LLM menjawab berdasarkan dokumen) ---")
    rag_pipeline(test_q)

    print(f"\n✅ Selesai! Memahami RAG pipeline.")
    print("\nAlur RAG:")
    print("  1. RETRIEVE: Cari dokumen yang relevan dari knowledge base")
    print("  2. AUGMENT: Masukkan dokumen ke prompt sebagai konteks")
    print("  3. GENERATE: LLM menjawab berdasarkan konteks (bukan mengarang)")

if __name__ == "__main__":
    main()
