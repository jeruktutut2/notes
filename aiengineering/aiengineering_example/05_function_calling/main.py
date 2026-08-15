"""
==============================================================================
CONTOH MODUL 5: FUNCTION / TOOL CALLING
==============================================================================
LLM pada dasarnya hanya penghasil teks. LLM tidak bisa mengeksekusi kalkulasi
keuangan yang akurat, tidak bisa mengecek database produk, dan tidak memiliki
akses internet real-time.

DENGAN FUNCTION / TOOL CALLING:
    Kita mendaftarkan fungsi-fungsi Python lokal sebagai "Tools" yang dapat dipanggil
    oleh LLM. Saat LLM membutuhkan aksi nyata, LLM merespon berupa perintah panggil fungsi
    beserta argumen parameter yang tepat.

ALUR 2-LANGKAH (2-STEP LOOP):
    Langkah 1: User bertindak -> Kirim pesan + daftar Tools ke LLM.
    Langkah 2: LLM mendeteksi butuh tool -> Mengembalikan nama fungsi & argumen JSON.
    Langkah 3: Sistem kita mengeksekusi fungsi Python asli.
    Langkah 4: Hasil eksekusi dikirim kembali ke LLM untuk menyusun kalimat respon akhir.

CARA PAKAI:
    - Jalankan: python main.py
==============================================================================
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL = os.getenv("DEFAULT_MODEL", "gemma3:4b")


# ------------------------------------------------------------------------------
# 1. DEFINISI FUNGSI PYTHON LOKAL (FUNGSI NYATA KITA)
# ------------------------------------------------------------------------------

def hitung_angsuran_pinjaman(jumlah_pinjaman: float, bunga_tahunan: float, tenor_tahun: int) -> dict:
    """Fungsi nyata untuk menghitung angsuran bulanan pokok + bunga."""
    total_bulan = tenor_tahun * 12
    bunga_bulanan = (bunga_tahunan / 100) / 12
    
    # Formula Anuitas sederha
    angsuran_per_bulan = (jumlah_pinjaman * (1 + (bunga_tahunan/100) * tenor_tahun)) / total_bulan
    
    return {
        "jumlah_pinjaman": jumlah_pinjaman,
        "tenor_bulan": total_bulan,
        "angsuran_per_bulan": round(angsuran_per_bulan, 2),
        "total_pembayaran": round(angsuran_per_bulan * total_bulan, 2)
    }


def cek_stok_gudang(kode_produk: str) -> dict:
    """Fungsi nyata simulasi cek database inventaris barang."""
    database_gudang = {
        "LAP-001": {"nama": "Laptop Asus ROG", "stok": 15, "lokasi": "Rak A-2"},
        "KMP-002": {"nama": "Keyboard Mechanical", "stok": 0, "lokasi": "Gudang Utama"},
        "MOU-003": {"nama": "Mouse Wireless Logitech", "stok": 42, "lokasi": "Rak B-1"}
    }
    
    data = database_gudang.get(kode_produk.upper(), None)
    if data:
        return {"status": "ditemukan", "kode": kode_produk, "detail": data}
    else:
        return {"status": "tidak_ditemukan", "pesan": f"Produk dengan kode {kode_produk} tidak ada."}


# ------------------------------------------------------------------------------
# 2. SCHEMAS METADATA TOOLS UNTUK LLM
# ------------------------------------------------------------------------------

TOOLS_DEFINITION = [
    {
        "type": "function",
        "function": {
            "name": "hitung_angsuran_pinjaman",
            "description": "Menghitung estimasi angsuran kpr/kredit bulanan berdasarkan pinjaman, bunga, dan tenor.",
            "parameters": {
                "type": "object",
                "properties": {
                    "jumlah_pinjaman": {"type": "number", "description": "Total uang yang dipinjam dalam Rupiah"},
                    "bunga_tahunan": {"type": "number", "description": "Persentase suku bunga per tahun (contoh 5.5 untuk 5.5%)"},
                    "tenor_tahun": {"type": "integer", "description": "Lama durasi pinjaman dalam satuan tahun"}
                },
                "required": ["jumlah_pinjaman", "bunga_tahunan", "tenor_tahun"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cek_stok_gudang",
            "description": "Mengecek ketersediaan stok barang di gudang berdasarkan Kode Produk.",
            "parameters": {
                "type": "object",
                "properties": {
                    "kode_produk": {"type": "string", "description": "Kode SKU unik produk (misal: LAP-001, MOU-003)"}
                },
                "required": ["kode_produk"]
            }
        }
    }
]


# Map nama fungsi string ke objek fungsi Python asli
MAP_FUNGSI = {
    "hitung_angsuran_pinjaman": hitung_angsuran_pinjaman,
    "cek_stok_gudang": cek_stok_gudang
}


# ------------------------------------------------------------------------------
# 3. PIPELINE TOOL CALLING EXECUTION
# ------------------------------------------------------------------------------

def jalankan_agent_tool_calling(user_query: str):
    print(f"\n=========================================================")
    print(f"USER QUERY: '{user_query}'")
    print("=========================================================")

    messages = [
        {"role": "system", "content": "Kamu adalah asisten keuangan & inventaris toko. Gunakan tools jika dibutuhkan."},
        {"role": "user", "content": user_query}
    ]

    # --- STEAP 1: Kirim Query + Tools ke LLM ---
    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS_DEFINITION,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        res_data = response.json()["message"]

        # Cek apakah LLM ingin memanggil Tool
        tool_calls = res_data.get("tool_calls", [])

        if not tool_calls:
            print("ℹ️ LLM menjawab langsung tanpa perlu memanggil tool:")
            print(res_data.get("content", ""))
            return

        # --- STEP 2: Eksekusi Tool Lokal oleh Kode Python ---
        messages.append(res_data)  # Simpan respon pembuka dari AI ke percakapan

        for call in tool_calls:
            nama_fungsi = call["function"]["name"]
            argumen_json = call["function"]["arguments"]
            
            print(f"\n🛠️ LLM Meminta Eksekusi Tool: '{nama_fungsi}'")
            print(f"   Parameter Parsed: {argumen_json}")

            fungsi_target = MAP_FUNGSI.get(nama_fungsi)
            if fungsi_target:
                # Eksekusi fungsi Python asli
                hasil_fungsi = fungsi_target(**argumen_json)
                print(f"   Hasil Eksekusi Fungsi Asli: {hasil_fungsi}")

                # Masukkan hasil eksekusi ke percakapan dengan role 'tool'
                messages.append({
                    "role": "tool",
                    "content": json.dumps(hasil_fungsi),
                    "name": nama_fungsi
                })

        # --- STEP 3: Kirim Balik Hasil Tool ke LLM untuk Respon Akhir ---
        payload_final = {
            "model": MODEL,
            "messages": messages,
            "stream": False
        }

        res_final = requests.post(OLLAMA_URL, json=payload_final, timeout=30)
        res_final.raise_for_status()
        
        jawaban_akhir = res_final.json()["message"]["content"]
        print("\n--- [JAWABAN AKHIR UNTUK USER] ---")
        print(jawaban_akhir)

    except Exception as e:
        print(f"❌ Error Tool Calling: {e}")


if __name__ == "__main__":
    print("=========================================================")
    print("CHATBOT INTERAKTIF: FUNCTION / TOOL CALLING (MODUL 5)")
    print("=========================================================")
    print("\nAsisten Siap! Anda bisa bertanya tentang perhitungan angsuran pinjaman")
    print("atau ketersediaan stok gudang (Misal: kode LAP-001, MOU-003, KMP-002).")
    print("Ketik 'keluar' atau 'exit' untuk berhenti.\n")

    while True:
        user_query = input("Kamu: ").strip()
        if user_query.lower() in ['keluar', 'exit', 'q']:
            print("Sampai jumpa!")
            break
        if not user_query:
            continue
            
        jalankan_agent_tool_calling(user_query)
        print("\n" + "-"*50)
