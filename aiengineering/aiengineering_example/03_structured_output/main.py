"""
==============================================================================
CONTOH MODUL 3: STRUCTURED OUTPUT DENGAN PYDANTIC
==============================================================================
Secara default, LLM mengembalikan teks narasi mentah (unstructured text).
Dalam pengembangan software nyata, kita membutuhkan data yang terstruktur
seperti JSON dengan tipe data pasti (integer, float, list, enum) untuk disimpan
ke database atau diproses oleh API lain.

SKENARIO DUNIA NYATA:
    Sistem parser nota/faktur pembelian otomatis dan pengkategorian tiket
    support pelanggan secara type-safe.

YANG DIPELAJARI:
    1. Membuat skema data dengan Pydantic (BaseModel, Field, Enum)
    2. Ekstraksi otomatis JSON Schema dari objek Pydantic
    3. Memaksa LLM menghasilkan JSON valid sesuai skema
    4. Validasi data dan penanganan kesalahan (Retry Logic jika format salah)

CARA PAKAI:
    - Jalankan: python main.py
==============================================================================
"""

import os
import json
import requests
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL = os.getenv("DEFAULT_MODEL", "gemma3:4b")


# ------------------------------------------------------------------------------
# 1. DEFINISI SKEMA PYDANTIC (STRUCTURED DATA MODEL)
# ------------------------------------------------------------------------------

class KategoriTiket(str, Enum):
    """Pilihan kategori terikat (Enum) untuk tiket customer service."""
    TEKNIS = "TEKNIS"
    TAGIHAN = "TAGIHAN"
    FITUR_BARU = "FITUR_BARU"
    UMUM = "UMUM"


class PrioritasEnum(str, Enum):
    TINGGI = "TINGGI"
    SEDANG = "SEDANG"
    RENDAH = "RENDAH"


class ItemBelanja(BaseModel):
    """Skema untuk item barang di dalam faktur/nota."""
    nama_item: str = Field(description="Nama barang yang dibeli")
    jumlah: int = Field(description="Kuantitas barang yang dibeli (harus berupa angka bulat)")
    harga_satuan: float = Field(description="Harga per item dalam Rupiah")


class LaporanNota(BaseModel):
    """Skema utama hasil ekstraksi nota pembelian."""
    nama_toko: str = Field(description="Nama merchant/toko tempat bertransaksi")
    tanggal: str = Field(description="Tanggal transaksi dalam format YYYY-MM-DD")
    daftar_item: List[ItemBelanja] = Field(description="Daftar item belanjaan")
    total_bayar: float = Field(description="Total biaya akhir yang dibayarkan")
    metode_pembayaran: Optional[str] = Field(default="CASH", description="Metode bayar (CASH, QRIS, KARTU_KREDIT)")


class AnalisisTiketCS(BaseModel):
    """Skema hasil analisa email/komplain pelanggan."""
    nama_pelanggan: str = Field(description="Nama pengirim pesan/pelanggan")
    kategori: KategoriTiket = Field(description="Klasifikasi masalah tiket")
    prioritas: PrioritasEnum = Field(description="Tingkat kedaruratan penanganan")
    ringkasan_masalah: str = Field(description="Ringkasan singkat keluhan dalam 1 kalimat")


# ------------------------------------------------------------------------------
# 2. FUNGSI EKSTRAKSI DENGAN PYDANTIC & RETRY LOGIC
# ------------------------------------------------------------------------------

def ekstraksi_data_terstruktur(teks_input: str, pydantic_class, max_retries: int = 3):
    """
    Fungsi generik yang meminta AI membaca teks bebas dan mengekstraknya
    menjadi objek Pydantic secara type-safe.

    Jika AI memberikan JSON yang salah format, fungsi ini melakukan RETRY otomatis
    sambil memberikan pesan kesalahan ke AI agar memperbaiki kodenya.
    """
    # Ambil JSON Schema otomatis dari Pydantic
    json_schema = json.dumps(pydantic_class.model_json_schema(), indent=2)

    system_prompt = f"""Kamu adalah parser data JSON otomatis yang sangat teliti.
Tugasmu adalah membaca teks input dari pengguna dan mengekstraknya menjadi JSON.

ATURAN WAJIB:
1. Output HANYA boleh berupa objek JSON valid yang mengikuti Skema JSON di bawah ini.
2. Jangan sertakan teks pengantar, penjelas, atau markdown ```json ... ```. HANYA JSON MURNI.

SKEMA JSON YANG HARUS DIIKUTI:
{json_schema}
"""

    history = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": teks_input}
    ]

    for percobaan in range(1, max_retries + 1):
        print(f"\n[Percobaan {percobaan}/{max_retries}] Mengirim request ekstraksi ke LLM...")
        
        payload = {
            "model": MODEL,
            "messages": history,
            "format": "json",  # Mode JSON Ollama API (memaksa output format JSON)
            "stream": False,
            "options": {"temperature": 0.0}  # Temp 0.0 wajib untuk determinisme struktur
        }

        try:
            res = requests.post(OLLAMA_URL, json=payload, timeout=30)
            res.raise_for_status()
            
            raw_json_str = res.json()["message"]["content"]
            print(f"Raw Output AI: {raw_json_str}")

            # --- VALIDASI PYDANTIC ---
            # Mengubah string JSON dari AI menjadi instance Pydantic Class yang tervalidasi
            objek_tervalidasi = pydantic_class.model_validate_json(raw_json_str)
            print("✅ Validasi Pydantic BERHASIL! Data terstruktur cocok dengan skema.")
            return objek_tervalidasi

        except ValidationError as val_err:
            print(f"⚠️ Validasi Pydantic Gagal: {val_err}")
            # Masukkan kesalahan ke history agar AI bisa memperbaiki pada iterasi berikutnya
            history.append({"role": "assistant", "content": raw_json_str})
            history.append({
                "role": "user", 
                "content": f"JSON yang kamu berikan tidak valid sesuai skema Pydantic!\nError: {val_err}\nPerbaiki dan berikan JSON murni!"
            })

        except Exception as e:
            print(f"❌ Error HTTP/Ollama: {e}")
            break

    return None


# ------------------------------------------------------------------------------
# 3. DEMO APELIKASI REAL-WORLD
# ------------------------------------------------------------------------------

def demo_parser_nota(teks_nota_bebas: str):
    print("\n--- [HASIL OBJEK PYTHON / PYDANTIC] ---")
    hasil_nota: LaporanNota = ekstraksi_data_terstruktur(teks_nota_bebas, LaporanNota)

    if hasil_nota:
        print(f"Toko: {hasil_nota.nama_toko}")
        print(f"Tanggal: {hasil_nota.tanggal}")
        print(f"Total Bayar: Rp {hasil_nota.total_bayar:,.2f}")
        print(f"Metode Pembayaran: {hasil_nota.metode_pembayaran}")
        print("Daftar Item:")
        for item in hasil_nota.daftar_item:
            print(f"  - {item.nama_item} | Qty: {item.jumlah} | Harga: Rp {item.harga_satuan:,.2f}")


def demo_analisis_tiket_cs(email_pelanggan: str):
    print("\n--- [HASIL EKSTRAKSI TIKET CS] ---")
    hasil_tiket: AnalisisTiketCS = ekstraksi_data_terstruktur(email_pelanggan, AnalisisTiketCS)

    if hasil_tiket:
        print(f"Pengirim : {hasil_tiket.nama_pelanggan}")
        print(f"Kategori : {hasil_tiket.kategori.value}")
        print(f"Prioritas: {hasil_tiket.prioritas.value}")
        print(f"Ringkasan: {hasil_tiket.ringkasan_masalah}")


if __name__ == "__main__":
    print("=========================================================")
    print("CHATBOT INTERAKTIF: STRUCTURED OUTPUT (MODUL 3)")
    print("=========================================================")
    
    while True:
        print("\nPilih Skenario Ekstraksi:")
        print("1. Parser Nota / Faktur Pembelian")
        print("2. Klasifikasi Tiket Customer Service")
        pilihan = input("Pilihan (1/2) atau 'keluar': ").strip()

        if pilihan.lower() in ['keluar', 'exit', 'q']:
            print("Sampai jumpa!")
            break
            
        if pilihan not in ['1', '2']:
            print("Pilihan tidak valid.")
            continue
            
        print("\nMasukkan teks bebas (ketik 'SELESAI' di baris baru untuk memproses):")
        lines = []
        while True:
            try:
                line = input()
                if line.strip().upper() == 'SELESAI':
                    break
                lines.append(line)
            except EOFError:
                break
            
        teks_input = "\n".join(lines)
        if not teks_input.strip():
            continue
            
        if pilihan == '1':
            demo_parser_nota(teks_input)
        elif pilihan == '2':
            demo_analisis_tiket_cs(teks_input)
        
        print("\n" + "-"*50)
