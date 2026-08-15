"""
==============================================================================
CONTOH MODUL 7: EVALUASI AI (EVALS WITH PYTEST & LLM-AS-A-JUDGE)
==============================================================================
Tidak seperti perangkat lunak tradisional yang memiliki output deterministik
(misal: assert 2 + 2 == 4), output LLM bersifat probabilistik.

EVALUASI AI (AI EVALS) ADALAH STRATEGI UNTUK:
    1. Memastikan kualitas output LLM tidak mengalami regresi (penurunan).
    2. Mengukur kepatuhan format data (JSON Schema Validation).
    3. Mengukur latensi respon (performance SLA).
    4. Menggunakan LLM sekunder sebagai penilai otomatis (LLM-as-a-Judge).

CARA PAKAI:
    - Jalankan dengan pytest: pytest 07_evals/test_ai.py -v -s
==============================================================================
"""

import os
import json
import time
import pytest
import requests
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL = os.getenv("DEFAULT_MODEL", "gemma3:4b")


# ------------------------------------------------------------------------------
# HELPER FUNCTION PEMANGGILAN LLM
# ------------------------------------------------------------------------------
def panggil_ai(prompt: str, system: str = "", format_json: bool = False, temperature: float = 0.0) -> str:
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature}
    }
    if format_json:
        payload["format"] = "json"

    res = requests.post(OLLAMA_URL, json=payload, timeout=30)
    res.raise_for_status()
    return res.json()["message"]["content"]


# ------------------------------------------------------------------------------
# 1. TEST CASE: EXACT MATCH & CONTAINMENT (AKURASI FASTER)
# ------------------------------------------------------------------------------
def test_klasifikasi_sentimen_positif():
    """Menguji apakah AI secara tepat memberikan klasifikasi sentimen POSITIF."""
    prompt = "Jawab HANYA 1 kata (POSITIF/NEGATIF/NETRAL): Saya sangat puas dengan pelayanan hotel ini!"
    respon = panggil_ai(prompt, temperature=0.0).strip()
    
    # Asserting exact match (mengabaikan kapitalisasi)
    assert "POSITIF" in respon.upper(), f"Diharapkan POSITIF tetapi mendapat: '{respon}'"


def test_ekstraksi_entitas_kata_kunci():
    """Menguji apakah AI berhasil menemukan nama kota dari kalimat."""
    prompt = "Ekstrak nama kota pengiriman dari kalimat: 'Paket dikirim ke alamat Jalan Sudirman No 12, Bandung Jawa Barat'."
    respon = panggil_ai(prompt, temperature=0.0)
    
    # Asserting substring containment
    assert "Bandung" in respon, f"Kata 'Bandung' harus ada pada jawaban: {respon}"


# ------------------------------------------------------------------------------
# 2. TEST CASE: VALIDASI STRUCTURAL JSON SCHEMA
# ------------------------------------------------------------------------------
class OutputProduk(BaseModel):
    nama_produk: str
    harga: float
    tersedia: bool


def test_format_json_valid():
    """Menguji apakah AI menghasilkan JSON yang sesuai dengan Pydantic Schema."""
    prompt = "Berikan info produk 'Sepatu Lari' seharga 450000 yang stoknya tersedia dalam format JSON."
    raw_json = panggil_ai(prompt, format_json=True, temperature=0.0)
    
    try:
        # Mencoba parse ke Pydantic
        objek = OutputProduk.model_validate_json(raw_json)
        assert objek.harga == 450000.0
        assert objek.tersedia is True
    except Exception as e:
        pytest.fail(f"Respon AI gagal divalidasi ke Schema Pydantic: {e}\nRaw JSON: {raw_json}")


# ------------------------------------------------------------------------------
# 3. TEST CASE: EVALUASI KINERJA LATENSI (SLA PERFORMANCE)
# ------------------------------------------------------------------------------
def test_latensi_respon():
    """Menguji bahwa waktu respon LLM tidak melebihi batas toleransi SLA (misal: 10 detik)."""
    start_time = time.time()
    _ = panggil_ai("Sebutkan 3 warna primer.", temperature=0.0)
    duration = time.time() - start_time
    
    print(f"\n⏱️ Durasi Latensi Respon AI: {duration:.2f} detik")
    assert duration < 10.0, f"Respon terlalu lambat! Membutuhkan {duration:.2f} detik."


# ------------------------------------------------------------------------------
# 4. TEST CASE: LLM-AS-A-JUDGE (EVALUATOR MODEL SEKERNDER)
# ------------------------------------------------------------------------------
def test_llm_as_judge_kualitas_penjelasan():
    """
    Menggunakan LLM untuk menilai kualitas penataan paragraf AI lain (Skor 1 - 5).
    """
    # 1. Minta AI pertama membuat penjelasan
    prompt_subjek = "Jelaskan apa ituPhotosynthesis dalam 2 kalimat sederhana untuk anak SD."
    jawaban_ai = panggil_ai(prompt_subjek)

    # 2. Minta LLM Penilai (Judge) memberikan nilai
    prompt_judge = f"""Kamu adalah Evaluator Kualitas Konten Edukasi.
Tugasmu adalah menilai jawaban berikut berdasarkan 2 kriteria:
1. Keakuratan fakta ilmiah.
2. Kejelasan untuk anak usia Sekolah Dasar (SD).

Pertanyaan Asli: {prompt_subjek}
Jawaban AI yang Dinilai: {jawaban_ai}

Berikan skor antara 1 sampai 5 (di mana 5 sangat bagus) dalam format JSON murni:
{{"skor": 5, "alasan": "Penjelasan sangat jernih dan mudah dipahami."}}
"""

    raw_judge_res = panggil_ai(prompt_judge, format_json=True, temperature=0.0)
    
    try:
        data_judge = json.loads(raw_judge_res)
        skor = data_judge.get("skor", 0)
        alasan = data_judge.get("alasan", "")

        print(f"\n👩‍⚖️ LLM Judge Score: {skor}/5 | Alasan: {alasan}")
        assert skor >= 4, f"Kualitas penjelasan dianggap rendah oleh Judge (Skor: {skor}). Alasan: {alasan}"

    except Exception as e:
        pytest.fail(f"Gagal memproses penilaian LLM-as-a-Judge: {e}")
