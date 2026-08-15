# 📖 CATATAN TEORI: MULTIMODAL AI TASKS & FRAMEWORKS

File ini berisi catatan teori komprehensif mengenai **7 Multimodal AI Tasks & SDK Frameworks** berdasarkan kurikulum [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer).

---

## 👁️ 1. OpenAI Vision API (GPT-4o)

GPT-4o adalah model multimodal native buatan OpenAI yang mampu memproses input teks, gambar, dan suara secara simultan.

### Parameter Penting Vision
- **Detail Mode (`low` vs `high`)**:
  - `low`: Mengompres gambar menjadi 512x512 piksel, hemat token (85 tokens).
  - `high`: Membagi gambar menjadi ubin (tiles) 512x512 piksel untuk ketelitian tinggi (OCR, grafik detail).
- **Base64 vs Image URL**:
  - Base64 berguna untuk gambar lokal tanpa server hosting publik.
  - Image URL efisien untuk gambar yang di-host di CDN.

---

## 🎨 2. DALL-E 3 API

DALL-E 3 terintegrasi secara otomatis dengan ChatGPT/GPT-4 untuk melakukan perbaikan prompt (*prompt rewriting/revision*).

### Parameter Utama
- `quality`: `"standard"` atau `"hd"`.
- `style`: `"vivid"` (hiper-realistik/dramatis) atau `"natural"` (foto alami).
- `response_format`: `"url"` atau `"b64_json"`.

---

## 🍌 3. NanoBanana API & Custom Multimodal REST Endpoints

Banyak perusahaan mengintegrasikan API multimodal terspesialisasi (seperti Gemini 1.5 Pro multimodal REST, Replicate API, atau NanoBanana API internal) untuk memproses data audio dan gambar dengan latensi rendah.

---

## 🎙️ 4. Whisper API

OpenAI Whisper API menyediakan 2 endpoint utama:
1. `/v1/audio/transcriptions`: Mengonversi audio ke teks bahasa asli.
2. `/v1/audio/translations`: Mengonversi audio dari bahasa apapun langsung ke Bahasa Inggris.

---

## 🤗 5. Hugging Face Models

1. **CLIP (OpenAI)**: Mengukur keselarasan (*similarity score*) antara gambar dan teks. Digunakan untuk Zero-Shot Image Classification dan Image Search.
2. **BLIP / BLIP-2 (Salesforce)**: Model untuk Image Captioning dan Visual Question Answering.
3. **Florence-2 (Microsoft)**: Model vision foundation serbaguna untuk Object Detection (`<OD>`), Captioning, dan Segmentation.

---

## 🦜🔗 6. LangChain for Multimodal Apps

LangChain mempermudah pembuatan rantai aplikasi multimodal melalui modul:
- `HumanMessage` dengan array payload item (`image_url`, `text`).
- `ChatPromptTemplate` berparameter dinamis untuk gambar.

---

## 🦙 7. LlamaIndex for Multimodal Apps

LlamaIndex menyediakan abstraksi tingkat tinggi untuk Multimodal RAG:
- `MultiModalVectorStoreIndex`: Mengelola indeks vektor terpisah untuk node teks dan node gambar.
- `SimpleMultiModalQueryEngine`: Menggabungkan retrieval gambar dan teks sebelum disintesis oleh Vision LLM.
