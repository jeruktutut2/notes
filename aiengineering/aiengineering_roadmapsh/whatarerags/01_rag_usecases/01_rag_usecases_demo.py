"""
01_rag_usecases_demo.py
Demostrasi Skenario & Kasus Penggunaan RAG (Retrieval-Augmented Generation)
"""

import sys

USE_CASES = {
    "1": {
        "title": "Enterprise HR Knowledge Base",
        "description": "Menjawab pertanyaan karyawan seputar SOP HR & Tunjangan Perusahaan.",
        "sample_query": "Berapa jatah cuti tahunan dan cuti hamil untuk karyawan tetap?",
        "mock_retrieved_context": [
            "[SOP HR 2024 - Bab 4] Karyawan tetap berhak atas 12 hari cuti tahunan per tahun setelah masa kerja 1 tahun.",
            "[SOP HR 2024 - Bab 4.2] Cuti melahirkan/hamil diberikan selama 3 bulan penuh dengan gaji dibayar 100%."
        ],
        "synthesized_response": "Berdasarkan SOP HR 2024 Bab 4 & 4.2:\n1. Cuti Tahunan: 12 hari per tahun untuk karyawan tetap setelah 1 tahun masa kerja.\n2. Cuti Melahirkan: 3 bulan penuh dengan gaji dibayar 100%."
    },
    "2": {
        "title": "Customer Support Chatbot E-Commerce",
        "description": "Menangani pertanyaan pengguna seputar status pesanan & pengembalian barang.",
        "sample_query": "Bagaimana prosedur pengembalian barang jika barang yang diterima cacat?",
        "mock_retrieved_context": [
            "[Kebijakan Retur - Pasal 2] Barang yang cacat dapat diretur maksimal 7 hari kerja setelah barang diterima.",
            "[Kebijakan Retur - Pasal 3] Pengguna wajib menyertakan video unboxing dan mengunggahnya ke menu Pusat Bantuan."
        ],
        "synthesized_response": "Prosedur pengembalian barang cacat (Kebijakan Retur Pasal 2 & 3):\n- Retur dapat diajukan maksimal 7 hari kerja sejak barang diterima.\n- Wajib menyertakan video unboxing saat mengunggah laporan di menu Pusat Bantuan."
    },
    "3": {
        "title": "Codebase Semantic QA (Developer Assistant)",
        "description": "Pencarian fungsi & arsitektur kode internal monorepo.",
        "sample_query": "Di mana fungsi untuk menghitung potongan diskon promo diimplementasikan?",
        "mock_retrieved_context": [
            "[services/discount.py:L15-32] def calculate_promo_discount(cart_total: float, promo_code: str) -> float:",
            "[services/discount.py:L40] Menggunakan algoritma tiered discount dan memvalidasi tanggal kedaluwarsa kupon."
        ],
        "synthesized_response": "Fungsi potongan diskon berada di `services/discount.py` pada fungsi `calculate_promo_discount(cart_total, promo_code)`. Fungsi ini menerapkan tiered discount dan mengecek validitas kupon."
    }
}

def run_usecase_demo(choice: str = None):
    print("=" * 70)
    print("🎯 DEMO KASUS PENGGUNAAN RAG (RAG USE CASES)")
    print("=" * 70)
    
    if not choice or choice not in USE_CASES:
        choice = "1"
        
    case = USE_CASES[choice]
    print(f"\n📌 Skenario: {case['title']}")
    print(f"📝 Deskripsi: {case['description']}")
    print(f"❓ Pertanyaan (Query): \"{case['sample_query']}\"")
    print("-" * 50)
    print("🔎 Dokumen/Konteks Yang Diambil (Retrieved Chunks):")
    for idx, ctx in enumerate(case["mock_retrieved_context"], 1):
        print(f"   [{idx}] {ctx}")
    print("-" * 50)
    print("🤖 Jawaban Hasil Sintesis RAG (Disertai Sumber):")
    print(case["synthesized_response"])
    print("=" * 70)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_usecase_demo(sys.argv[1])
    else:
        for key in USE_CASES:
            run_usecase_demo(key)
