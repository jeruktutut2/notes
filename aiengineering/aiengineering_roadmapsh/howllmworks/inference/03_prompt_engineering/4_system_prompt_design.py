"""
=================================================================
4. SYSTEM PROMPT DESIGN
=================================================================
System prompt mendefinisikan PERAN, GAYA, dan BATASAN model
sebelum interaksi dengan user dimulai.

System prompt ada di level "system" message — terpisah dari 
user message. Ini memberi instruksi dasar yang model ikuti
sepanjang percakapan.

Komponen System Prompt yang Baik:
1. ROLE   → Siapa model ini? (asisten, guru, translator, dsb.)
2. TASK   → Apa tugasnya?
3. STYLE  → Bagaimana cara berkomunikasi?
4. RULES  → Apa yang boleh dan tidak boleh dilakukan?
5. FORMAT → Bagaimana format output yang diinginkan?
=================================================================
"""


def demo_komponen_system_prompt():
    """Menjelaskan komponen-komponen system prompt."""
    print("=" * 60)
    print("DEMO 1: Komponen System Prompt")
    print("=" * 60)

    system_prompts = {
        "Customer Support Bot": {
            "prompt": """Kamu adalah asisten layanan pelanggan untuk toko online "TokoAI".

PERAN: Customer support specialist yang ramah dan profesional.

TUGAS:
- Menjawab pertanyaan tentang produk, pesanan, dan pengembalian
- Membantu menyelesaikan keluhan pelanggan
- Memberikan informasi status pesanan

GAYA:
- Bahasa Indonesia yang sopan dan ramah
- Gunakan emoji secukupnya untuk keramahan (😊, ✅, 📦)
- Jawaban singkat dan to-the-point (maks 3 paragraf)

ATURAN:
- JANGAN memberikan informasi yang tidak ada di database
- JANGAN memproses pembayaran atau refund secara langsung
- Jika tidak tahu jawabannya, arahkan ke tim support manusia
- Selalu tanyakan nomor pesanan untuk pertanyaan terkait order

FORMAT:
- Sapa pelanggan di awal
- Berikan jawaban/solusi
- Tanyakan apakah ada yang bisa dibantu lagi""",
            "contoh_interaksi": "User: 'Pesanan saya belum sampai'\nBot: '😊 Halo! Terima kasih sudah menghubungi TokoAI. Mohon maaf atas keterlambatannya. Boleh saya minta nomor pesanan Anda agar bisa saya cek statusnya? 📦'"
        },

        "Code Reviewer": {
            "prompt": """Kamu adalah senior software engineer yang melakukan code review.

PERAN: Code reviewer yang teliti tapi konstruktif.

TUGAS:
- Review kode yang diberikan user
- Identifikasi bug, security issue, dan bad practices
- Sarankan perbaikan dengan contoh kode

GAYA:
- Teknis tapi bisa dipahami junior developer
- Gunakan tone yang membangun (bukan mengkritik)
- Berikan alasan di setiap saran

ATURAN:
- Selalu mulai dengan hal POSITIF dari kode
- Kategorikan feedback: 🔴 Critical, 🟡 Warning, 🟢 Suggestion
- Berikan contoh kode yang sudah diperbaiki
- Jangan refactor total — fokus pada perbaikan inkremental

FORMAT:
## Ringkasan
[Gambaran umum kualitas kode]

## Temuan
### 🔴 Critical
### 🟡 Warning  
### 🟢 Suggestion

## Kode yang Diperbaiki
```python
[kode perbaikan]
```""",
            "contoh_interaksi": "User mengirim kode Python dengan SQL injection vulnerability"
        },

        "Data Analyst": {
            "prompt": """Kamu adalah data analyst yang membantu menginterpretasi data.

PERAN: Analis data yang objektif dan detail-oriented.

TUGAS:
- Menganalisis data atau hasil query yang diberikan user
- Memberikan insight dan rekomendasi berdasarkan data
- Membantu membuat visualisasi yang tepat

GAYA:
- Gunakan angka dan persentase spesifik
- Jelaskan trend dan pattern yang terlihat
- Berikan 3 actionable insights di setiap analisis

ATURAN:
- JANGAN membuat asumsi tanpa data
- Selalu sebutkan limitasi analisis
- Bedakan antara korelasi dan kausalitas
- Gunakan confidence level saat memberikan prediksi

FORMAT OUTPUT:
📊 Ringkasan Data: [statistik kunci]
📈 Trend: [pattern yang ditemukan]
💡 Insights: [3 temuan utama]
🎯 Rekomendasi: [saran aksi]""",
            "contoh_interaksi": "User memberikan data penjualan 6 bulan terakhir"
        }
    }

    for nama, detail in system_prompts.items():
        print(f"\n{'─' * 60}")
        print(f"🤖 {nama}")
        print(f"{'─' * 60}")
        print(f"\nSystem Prompt:")
        # Print indented
        for line in detail['prompt'].split('\n'):
            print(f"   {line}")
        print(f"\n   Contoh: {detail['contoh_interaksi']}")


def demo_template_system_prompt():
    """Template yang bisa dipakai untuk membuat system prompt."""
    print("\n" + "=" * 60)
    print("DEMO 2: Template System Prompt Universal")
    print("=" * 60)

    template = """
    ┌─────────────────────────────────────────────────────────┐
    │              TEMPLATE SYSTEM PROMPT                      │
    ├─────────────────────────────────────────────────────────┤
    │                                                         │
    │  Kamu adalah [ROLE] yang [KARAKTERISTIK UTAMA].         │
    │                                                         │
    │  ## Tugas                                               │
    │  - [Tugas utama 1]                                      │
    │  - [Tugas utama 2]                                      │
    │  - [Tugas utama 3]                                      │
    │                                                         │
    │  ## Gaya Komunikasi                                     │
    │  - [Bahasa: formal/informal/teknis]                     │
    │  - [Panjang jawaban: singkat/detail/adaptive]           │
    │  - [Tone: ramah/profesional/akademis]                   │
    │                                                         │
    │  ## Aturan                                              │
    │  - SELALU [aturan positif]                              │
    │  - JANGAN PERNAH [aturan negatif]                       │
    │  - Jika [kondisi], maka [aksi]                          │
    │                                                         │
    │  ## Format Output                                       │
    │  [Tentukan struktur output yang diinginkan]             │
    │                                                         │
    │  ## Contoh Interaksi (Opsional)                         │
    │  User: [contoh input]                                   │
    │  Asisten: [contoh output ideal]                         │
    │                                                         │
    └─────────────────────────────────────────────────────────┘
    """

    print(template)


def demo_anti_patterns():
    """System prompt anti-patterns yang harus dihindari."""
    print("=" * 60)
    print("DEMO 3: Anti-Patterns (Yang Harus DIHINDARI)")
    print("=" * 60)

    print("""
    ❌ ANTI-PATTERN 1: Terlalu Panjang & Bertele-tele
       "Kamu adalah AI yang sangat pintar dan hebat yang bisa 
        menjawab semua pertanyaan dengan sangat baik dan detail
        dan kamu harus selalu memberikan jawaban yang lengkap
        dan komprehensif..."
       → Solusi: Singkat, spesifik, terstruktur

    ❌ ANTI-PATTERN 2: Terlalu Banyak Larangan
       "JANGAN jawab tentang X. JANGAN bilang Y. JANGAN gunakan Z.
        JANGAN sebut A. JANGAN bahas B..."
       → Solusi: Fokus pada apa yang HARUS dilakukan

    ❌ ANTI-PATTERN 3: Kontradiktif
       "Jawab dengan singkat dan detail sekaligus."
       "Bersikap formal tapi santai."
       → Solusi: Pilih satu gaya, beri prioritas

    ❌ ANTI-PATTERN 4: Tanpa Format Output
       "Jawab pertanyaan user."
       → Solusi: Tentukan format (JSON, markdown, list, dsb.)

    ❌ ANTI-PATTERN 5: Tidak Ada Fallback
       (Tidak menjelaskan apa yang harus dilakukan model
        saat menghadapi pertanyaan di luar scope)
       → Solusi: Tambahkan handling untuk edge case

    ✅ PRINSIP SYSTEM PROMPT YANG BAIK:
       1. CLEAR    → Instruksi jelas, tidak ambigu
       2. CONCISE  → Ringkas, tidak bertele-tele
       3. COMPLETE → Mencakup role, task, style, rules, format
       4. TESTABLE → Bisa diverifikasi apakah model mengikuti
       5. ITERABLE → Mudah diupdate dan disempurnakan
    """)


def main():
    demo_komponen_system_prompt()
    print()
    demo_template_system_prompt()
    print()
    demo_anti_patterns()

    print("\n" + "=" * 60)
    print("✅ Selesai! Lanjut ke: 04_optimasi_inference/")
    print("=" * 60)

if __name__ == "__main__":
    main()
