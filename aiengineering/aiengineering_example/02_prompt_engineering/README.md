# 📘 Modul 2 — Prompt Engineering

Modul ini mempelajari berbagai **teknik Prompt Engineering** mutakhir untuk mengarahkan cara berpikir dan gaya output Large Language Model (LLM).

---

## 🎯 Teknik-Teknik Utama yang Dipelajari

| Teknik | Deskripsi | Kapan Digunakan |
|---|---|---|
| **Zero-Shot** | Meminta AI mengerjakan tugas tanpa contoh pendahulu. | Untuk tugas sederhana dan model yang sudah sangat pintar. |
| **Few-Shot** | Menyediakan contoh *Input -> Output* di awal prompt. | Untuk memformat struktur data secara khusus atau klasifikasi. |
| **Chain-of-Thought (CoT)** | Mengarahkan AI berpikir "Langkah demi Langkah" (step-by-step). | Untuk masalah penalaran matematika, logika kompleks, atau pemecahan masalah. |
| **Role Prompting** | Memberi identitas spesifik di System Prompt (misal: Chef, Auditor). | Untuk menyesuaikan nada, terminologi teknis, dan gaya bahasa. |
| **Temperature Control** | Mengatur tingkat acak/kreativitas (0.0 s/d 1.0). | Temp 0.0 untuk data faktual/kode; Temp 1.0 untuk karya kreatif/slogan. |

---

## 🚀 Cara Menjalankan (Oleh Pengguna)

```bash
# Pastikan Ollama sudah berjalan
ollama serve

# Jalankan script pengujian prompt
python 02_prompt_engineering/main.py
```
