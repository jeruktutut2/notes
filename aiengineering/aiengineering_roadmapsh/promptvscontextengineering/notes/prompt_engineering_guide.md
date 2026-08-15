# Panduan Lengkap Prompt Engineering (AI Engineering Roadmap)

Panduan ini mendokumentasikan konsep dasar hingga lanjutan **Prompt Engineering** berdasarkan kurikulum [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer).

---

## 1. Anatomi & Komponen Prompt

Setiap prompt yang siap dipakai di lingkungan produksi harus memiliki struktur terisolasi menggunakan **XML Delimiters** untuk mencegah *Instruction Drift* dan *Prompt Injection*.

```xml
<system_persona>
Anda adalah pakar AI Engineer yang bertugas menganalisis arsitektur LLM.
</system_persona>

<instruction>
Evaluasi arsitektur di bawah ini dan berikan poin kelebihan serta kelemahannya.
</instruction>

<context>
Sistem ini menggunakan RAG berbasis Qdrant dengan model embedding text-embedding-3-small.
</context>

<user_input>
Bagaimana cara mengurangi latensi Time-To-First-Token (TTFT)?
</user_input>

<output_constraint>
Jawab dalam format JSON dengan kunci: ["analysis", "latency_optimization_steps", "recommended_tools"].
</output_constraint>
```

### 4 Komponen Utama:
1. **Persona & System Framing**: Menentukan identitas, nada suara, dan batasan tanggung jawab model.
2. **Instruction / Task**: Perintah spesifik aksi yang harus dilakukan (misal: analisis, ekstraksi, terjemahkan).
3. **Context / Reference Data**: Informasi pendukung, dokumen RAG, atau aturan bisnis eksternal.
4. **Output Constraint**: Aturan batasan format luaran (JSON Schema, XML, Markdown Table).

---

## 2. Taksonomi Teknik Prompting

| Teknik Prompting | Deskripsi Singkat | Kasus Penggunaan Ideal |
|------------------|-------------------|------------------------|
| **Zero-Shot** | Memberikan instruksi langsung tanpa contoh sebelumnya. | Klasifikasi sederhana, Q&A umum. |
| **Few-Shot** | Memberikan 2-5 contoh pasangan (Input -> Output) di dalam prompt. | Formatisasi data kustom, klasifikasi domain khusus. |
| **Chain-of-Thought (CoT)** | Meminta LLM menyusun penalaran *step-by-step* sebelum jawaban akhir. | Pemecahan masalah matematika, logika, kode program. |
| **Self-Consistency Voting** | Menggenerasi multiple CoT paths lalu mengambil suara mayoritas (*majority vote*). | Tugas penalaran kompleks berakurasi tinggi. |
| **Tree-of-Thoughts (ToT)** | Mengeksplorasi cabang-cabang keputusan secara pohon (*tree search*). | Perencanaan strategis, algoritma pencarian. |
| **ReAct Framework** | Siklus interaktif *Thought -> Action -> Observation* dengan alat eksternal (APIs/Search). | AI Agents, pemanggilan Function Calling / Tools. |

---

## 3. Security, Red Teaming & Guardrails

Prompt Engineering di tingkat produksi membutuhkan pertahanan berlapis terhadap serangan keamanan LLM:

1. **Direct Prompt Injection**: Pengguna mencoba menimpa (*override*) instruksi sistem (contoh: *"Ignore previous instructions..."*).
2. **Indirect Prompt Injection**: Data dari luar (misal: dokumen web RAG) terselip instruksi jahat (*"Tampilkan data rahasia..."*).
3. **Sandwich Defense Pattern**: Mengurung data input pengguna di antara dua blok instruksi penjaga sistem (*system guardrails*).
4. **JSON Schema Repair Loop**: Validasi output JSON menggunakan Pydantic/Regex; jika rusak, jalankan skrip *auto-repair prompt* secara sekuensial.

---

## 4. Evaluasi & Metrik Prompt

- **LLM-as-a-Judge**: Menggunakan LLM terkuat (misal: GPT-4o) untuk menilai kualitas luaran prompt berbasis rubrik.
- **Semantic Similarity / BERTScore**: Mengukur kemiripan makna antara jawaban model dengan *ground truth*.
- **Pass@K Benchmark**: Mengukur proporsi generasi yang lulus pengujian kode/format dari $K$ percobaan.
