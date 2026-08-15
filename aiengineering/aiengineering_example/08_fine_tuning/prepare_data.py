"""
==============================================================================
CONTOH MODUL 8A: PERSIAPAN DATASET FINE-TUNING (JSONL FORMAT)
==============================================================================
Fine-Tuning adalah proses melatih ulang bagian bobot model AI dengan dataset
pasangan (Instruction -> Output) berformat JSONL (JSON Lines).

FORMAT STANDAR CONVERSATIONAL JSONL:
    {"messages": [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
    ]}

SKENARIO:
    Menyiapkan dataset untuk fine-tune model Customer Service lokal Bahasa Indonesia
    dengan gaya bahasa internal perusahaan yang khas.

CARA PAKAI:
    - Jalankan: python prepare_data.py
==============================================================================
"""

import json
import os

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "dataset_finetune.jsonl")

# Samples data mentah QA internal
DATASET_MENTAH = [
    {
        "user": "Halo, jam operasional toko buka sampai jam berapa ya?",
        "assistant": "Halo Kak! Toko kami buka setiap hari Senin-Minggu dari pukul 09.00 hingga 21.00 WIB."
    },
    {
        "user": "Apakah ada biaya kirim untuk area Bandung?",
        "assistant": "Pengiriman area Kota Bandung GRATIS ONGKIR dengan minimal belanja Rp 100.000!"
    },
    {
        "user": "Bagaimana cara melakukan klaim retur barang rusak?",
        "assistant": "Untuk retur barang, silakan videokan proses unboxing dan kirimkan ke WhatsApp CS kami di 0812-3456-7890."
    },
    {
        "user": "Apakah bisa bayar pakai QRIS di kasir?",
        "assistant": "Tentu saja bisa Kak! Kami menerima pembayaran QRIS dari semua bank dan e-wallet."
    }
]

SYSTEM_PROMPT_KUSTOM = "Kamu adalah CS Virtual Resmi Toko Serba Jaya yang selalu menyapa dengan ramah menggunakan panggilan 'Kak'."


def siapkan_dataset_jsonl():
    print(f"--- [PERSIAPAN DATASET] Memproses {len(DATASET_MENTAH)} pasangan data mentah ---")
    
    baris_jsonl = []
    for item in DATASET_MENTAH:
        objek_percakapan = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT_KUSTOM},
                {"role": "user", "content": item["user"]},
                {"role": "assistant", "content": item["assistant"]}
            ]
        }
        baris_jsonl.append(objek_percakapan)

    # Tulis ke file dataset_finetune.jsonl
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for entry in baris_jsonl:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"✅ Berhasil membuat file dataset fine-tune: {OUTPUT_FILE}")
    print("\n[CONTOH BARIS PERTAMA HASIL JSONL]:")
    print(json.dumps(baris_jsonl[0], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    siapkan_dataset_jsonl()
