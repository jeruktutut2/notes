# Catatan Roadmap AI Agents - Berdasarkan roadmap.sh/ai-agents

Berikut adalah konsep-konsep utama yang perlu dipelajari untuk memahami dan membangun AI Agent,
berdasarkan roadmap dari roadmap.sh.

## 1. LLM Fundamentals (Fondasi - "Otak" Agent)
Sebelum membangun agent, pahami dulu mesin reasoning-nya: Large Language Model (LLM).
*   **Apa yang dipelajari:**
    *   Cara memanggil LLM via API (OpenAI-compatible API).
    *   Parameter generasi: Temperature, Top-P, Max Tokens, Stop Sequences.
    *   Tokenization: Bagaimana teks dipecah menjadi token, context window, dan biaya per-token.
    *   Jenis model: Reasoning vs. Standard, Open-weight vs. Closed-weight.
*   **Implementasi Kode (Python):**
    *   Menggunakan library `openai` untuk memanggil API chat completion.
    *   Menggunakan `tiktoken` untuk menghitung jumlah token dari sebuah teks.
    *   Eksperimen dengan berbagai parameter (temperature rendah vs tinggi).

## 2. Prompt Engineering (Teknik Membuat Prompt)
Cara berkomunikasi dengan LLM secara efektif agar mendapatkan output yang diinginkan.
*   **Apa yang dipelajari:**
    *   Role-based prompting: System, User, Assistant messages.
    *   Chain-of-Thought (CoT): Meminta model berpikir langkah demi langkah.
    *   Few-shot prompting: Memberikan contoh di dalam prompt.
    *   Structured output: Meminta model mengeluarkan JSON atau format terstruktur.
*   **Implementasi Kode (Python):**
    *   Menyusun pesan dengan role system/user/assistant.
    *   Menerapkan teknik CoT untuk soal logika/matematika.
    *   Menggunakan `response_format` untuk memaksa output JSON.

## 3. Tools & Function Calling
Memberikan "tangan" kepada LLM agar bisa berinteraksi dengan dunia luar (API, database, file system).
*   **Apa yang dipelajari:**
    *   Mendefinisikan tool schema (nama, deskripsi, parameter) dalam format JSON.
    *   Memahami alur function calling: LLM meminta → kita eksekusi → kembalikan hasil.
    *   Menangani multiple tools dalam satu percakapan.
*   **Implementasi Kode (Python):**
    *   Mendefinisikan tools sebagai dict/list Python.
    *   Mengeksekusi function berdasarkan respons LLM.
    *   Membangun agent sederhana yang bisa memilih dari beberapa tools.

## 4. Agent Loop (Siklus Agent: Perception → Plan → Act → Observe)
Inti dari AI Agent: sebuah loop di mana agent menerima input, berpikir, bertindak, dan mengamati hasilnya secara berulang.
*   **Apa yang dipelajari:**
    *   Pola ReAct (Reasoning + Acting): Agent berpikir (Thought), memilih aksi (Action), mendapat hasil (Observation), lalu berpikir lagi.
    *   Kondisi berhenti (stopping criteria): Kapan agent harus menghentikan loop.
    *   Error handling: Apa yang dilakukan agent jika tool gagal.
*   **Implementasi Kode (Python):**
    *   Menulis agent loop manual (while loop + LLM call + tool execution).
    *   Implementasi pola ReAct dengan format Thought/Action/Observation.

## 5. Memory (Memori Agent)
Memungkinkan agent mengingat percakapan sebelumnya dan informasi jangka panjang.
*   **Apa yang dipelajari:**
    *   **Short-term memory:** Riwayat percakapan di dalam prompt (conversation history).
    *   **Summary memory:** Meringkas percakapan panjang agar muat di context window.
    *   **Long-term memory:** Menyimpan informasi ke vector database untuk dicari nanti.
    *   Episodic vs. Semantic memory.
*   **Implementasi Kode (Python):**
    *   Mengelola list messages sebagai riwayat percakapan.
    *   Memanggil LLM untuk meringkas percakapan panjang.
    *   Menggunakan ChromaDB untuk menyimpan dan mencari memori berbasis embedding.

## 6. RAG (Retrieval-Augmented Generation)
Menghubungkan LLM dengan sumber pengetahuan eksternal agar jawaban lebih akurat dan up-to-date.
*   **Apa yang dipelajari:**
    *   Embedding: Mengubah teks menjadi vektor numerik.
    *   Similarity search: Mencari dokumen yang paling relevan berdasarkan vektor.
    *   Chunking: Memecah dokumen panjang menjadi potongan kecil.
    *   Pipeline RAG: Query → Retrieve → Augment prompt → Generate.
*   **Implementasi Kode (Python):**
    *   Menghitung cosine similarity antar embedding.
    *   Membangun RAG pipeline sederhana dari nol.
    *   Implementasi text chunking dengan overlap.

## 7. Multi-Agent Systems
Menggabungkan beberapa agent yang bekerja sama untuk menyelesaikan tugas kompleks.
*   **Apa yang dipelajari:**
    *   Sequential agents: Agent A → Agent B → Agent C (pipeline).
    *   Supervisor pattern: Satu agent mendelegasikan tugas ke agent spesialis.
    *   Komunikasi antar agent: Bagaimana output satu agent menjadi input agent lain.
*   **Implementasi Kode (Python):**
    *   Membangun pipeline agent berantai (penulis → editor → reviewer).
    *   Membangun supervisor agent yang mendelegasikan tugas.

## 8. Guardrails & Safety (Keamanan Agent)
Memastikan agent berperilaku aman, tidak dimanipulasi, dan menghasilkan output yang bertanggung jawab.
*   **Apa yang dipelajari:**
    *   Prompt injection: Serangan di mana user mencoba mengubah perilaku agent.
    *   Input validation: Memfilter input berbahaya sebelum dikirim ke LLM.
    *   Output guardrails: Mengecek output agent sebelum dikirim ke user.
    *   Content moderation: Memfilter konten sensitif/berbahaya.
*   **Implementasi Kode (Python):**
    *   Implementasi filter input (regex, keyword blocking, LLM-based detection).
    *   Implementasi output checker (PII detection, format validation).

## 9. Evaluasi & Observability (Monitoring Agent)
Mengukur dan memantau performa agent di production.
*   **Apa yang dipelajari:**
    *   Evaluasi otomatis: Menggunakan LLM untuk menilai output agent (LLM-as-judge).
    *   Metrik agent: Task completion rate, latency, cost per query.
    *   Logging & Tracing: Mencatat setiap langkah agent untuk debugging.
*   **Implementasi Kode (Python):**
    *   Membangun evaluator sederhana menggunakan LLM.
    *   Implementasi logger yang mencatat setiap step agent.
