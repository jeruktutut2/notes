# 01 - Closed Models (Proprietary Models)

 Closed Models (Model Hak Cipta / Proprietary) adalah model kecerdasan buatan di mana bobot (*weights*), data pelatihan, dan detail arsitektur internal tidak dipublikasikan secara umum. Pengguna mengakses model ini melalui API berbayar atau infrastruktur terkelola provider.

---

## 🏛️ Lanskap Closed Models Utama

### 1. Anthropic Claude
* **Model Unggulan**: Claude 3.5 Sonnet, Claude 3 Opus, Claude 3.5 Haiku.
* **Kekuatan Utama**:
  * **Kemampuan Reasoning & Coding**: Terkenal sangat superior untuk pembuatan kode kompleks, refactoring, dan analisis logika teknis.
  * **Jendela Konteks Besar**: Mendukung hingga 200,000 token dengan tingkat *retrieval accuracy* (Needle In A Haystack) mendekati 100%.
  * **Feature Highlights**: *Prompt Caching* (menghemat biaya hingga 90% dan menurunkan latensi hingga 85% pada instruksi berulang) dan *Computer Use* (kemampuan agen mengendalikan interface OS).
* **Kasus Penggunaan Terbaik**: Enterprise coding assistants, dokumen analisis panjang (hukum/keuangan), agen otonom.

### 2. Google Gemini
* **Model Unggulan**: Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 1.0 Ultra.
* **Kekuatan Utama**:
  * **Native Multimodality**: Dibangun dari awal (*native*) untuk memahami teks, gambar, audio, dan video secara bersamaan tanpa adapter terpisah.
  * **Ultra-Long Context Window**: Mendukung konteks hingga **1 hingga 2 Juta Token** (bahkan eksperimental 10M token), memungkinkan analisis jam rekaman video atau jutaan baris kode sekaligus.
  * **Integrasi Ekosistem Google**: Integrasi mulus dengan Google Cloud Platform (Vertex AI), Google Workspace, dan Firebase.
* **Kasus Penggunaan Terbaik**: Analisis multimodal (video audit, pemrosesan dokumen bergambar/PDF masif), aplikasi real-time latensi rendah (Flash model), enterprise GCP.

### 3. OpenAI (GPT & o-Series)
* **Model Unggulan**: GPT-4o, GPT-4o-mini, o1 (Reasoning), o3-mini.
* **Kekuatan Utama**:
  * **Struktur API & Ekosistem Terluas**: Mendukung *Structured Outputs* (Jaminan skema JSON presisi 100%), Vision, Realtime Audio API, dan Custom GPTs.
  * **o-Series (Reasoning Models)**: Menggunakan paradigma *Chain-of-Thought (CoT) Inference Time Search* untuk memecahkan masalah matematika, olimpiade sains, dan riset ilmiah kompleks yang gagal diselesaikan model standar.
* **Kasus Penggunaan Terbaik**: Aplikasi konsumen skala masif, integrasi function calling rumit, problem solving matematika/sains tingkat tinggi.

### 4. Cohere
* **Model Unggulan**: Command R+, Command R, Embed v3, Rerank 3.
* **Kekuatan Utama**:
  * **Enterprise RAG Specialist**: Dirancang khusus untuk pencarian informasi korporat, *Retrieval-Augmented Generation* (RAG), serta dukungan multibahasa industri.
  * **Citations & Grounding**: Menghasilkan kutipan (*citations*) otomatis dari dokumen sumber untuk mencegah halusinasi.
* **Kasus Penggunaan Terbaik**: Enterprise Knowledge Search, Semantic Search & Reranking sistem pencarian internal perusahaan.

### 5. Mistral (Commercial Offerings)
* **Model Unggulan**: Mistral Large 2, Mistral NeMo, Codestral.
* **Kekuatan Utama**:
  * **Efisiensi & Kinerja Tinggi**: Performa sekelas GPT-4 dengan ukuran token efisien dan biaya kompetitif.
  * **Kedaulatan Data Uni Eropa (EU Sovereignty)**: Pilihan ideal bagi organisasi di Eropa yang memerlukan kepatuhan GDPR ketat.
* **Kasus Penggunaan Terbaik**: Enterprise deployment di Eropa, aplikasi coding multibahasa.

---

## 📊 Tabel Perbandingan Closed Models

| Provider | Model Utama | Context Window | Kekuatan Utama | Fitur Spesial |
| :--- | :--- | :--- | :--- | :--- |
| **Anthropic** | Claude 3.5 Sonnet | 200K Tokens | Reasoning, Coding, Analysis | Prompt Caching, Artifacts, Computer Use |
| **Google** | Gemini 1.5 Pro | 2M Tokens | Native Multimodal (Video/Audio/Text) | Audio/Video input langsung, System Instruction |
| **OpenAI** | GPT-4o / o1 | 128K Tokens | General Capability, Math Reasoning | Structured Outputs (JSON Schema), Realtime API |
| **Cohere** | Command R+ | 128K Tokens | Enterprise RAG & Multi-step Tools | Grounded Citations, Native Rerank |
| **Mistral** | Mistral Large 2 | 128K Tokens | Multilingual Reasoning, Code | EU GDPR Compliance & Deployment |

---

## 🎯 Panduan Memilih Closed Model
1. **Pilih Claude 3.5 Sonnet** jika aplikasi Anda sangat bergantung pada pembuatan kode yang bersih, penganalisisan dokumen bisnis kompleks, atau penghematan biaya melalui Prompt Caching.
2. **Pilih Gemini 1.5 Pro/Flash** jika Anda mengolah input multimodal (misalnya analisis video 1 jam, file audio podcast, atau PDF 1.000 halaman) atau butuh latensi kilat harga terjangkau.
3. **Pilih OpenAI GPT-4o / o1** jika Anda memerlukan ekosistem tooling terlengkap, keluaran JSON presisi tinggi dengan Pydantic/JSON Schema, atau kemampuan pemecahan masalah penalaran logis tinggi.
4. **Pilih Cohere** untuk solusi pencarian dokumen internal (*RAG*) perusahaan yang membutuhkan penjelas sumber (*citation*) presisi.
