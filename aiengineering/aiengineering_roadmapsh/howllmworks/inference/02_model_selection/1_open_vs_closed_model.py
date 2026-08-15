"""
=================================================================
1. OPEN-SOURCE vs CLOSED MODEL
=================================================================
Dalam AI Engineering, ada 2 kategori besar model:

A) CLOSED / PROPRIETARY API
   - Model diakses via API (tidak bisa diunduh)
   - Contoh: OpenAI GPT-4, Anthropic Claude, Google Gemini
   - Kelebihan: Performa tinggi, mudah digunakan
   - Kekurangan: Biaya per token, data dikirim ke vendor

B) OPEN-SOURCE / OPEN-WEIGHT
   - Model bisa diunduh dan dijalankan sendiri
   - Contoh: Meta Llama, Mistral, Google Gemma, Qwen
   - Kelebihan: Gratis, privasi data, bisa fine-tune
   - Kekurangan: Perlu hardware, setup lebih kompleks

Kapan pakai yang mana?
┌─────────────────────────┬────────────────┬─────────────────┐
│ Kebutuhan               │ Open-Source    │ Closed API      │
├─────────────────────────┼────────────────┼─────────────────┤
│ Prototipe cepat         │                │ ✅              │
│ Data sensitif/privasi   │ ✅             │                 │
│ Budget terbatas (awal)  │ ✅             │                 │
│ Kualitas maksimal       │                │ ✅              │
│ Perlu fine-tuning       │ ✅             │                 │
│ Tidak punya GPU         │                │ ✅              │
│ Edge/offline deployment │ ✅             │                 │
│ Skalabilitas tinggi     │ ✅ (self-host) │ ✅ (pay-as-go)  │
└─────────────────────────┴────────────────┴─────────────────┘
=================================================================
"""


def bandingkan_model():
    """Menampilkan perbandingan model populer di setiap kategori."""
    print("=" * 70)
    print("PERBANDINGAN MODEL OPEN-SOURCE vs CLOSED API")
    print("=" * 70)

    closed_models = [
        {
            "nama": "GPT-4o (OpenAI)",
            "tipe": "CLOSED API",
            "parameter": "Tidak dipublikasi",
            "keunggulan": "Multi-modal, reasoning kuat, ecosystem luas",
            "biaya": "~$2.50/1M input tokens, ~$10/1M output tokens",
            "use_case": "Chatbot canggih, code generation, analisis dokumen"
        },
        {
            "nama": "Claude 3.5 Sonnet (Anthropic)",
            "tipe": "CLOSED API",
            "parameter": "Tidak dipublikasi",
            "keunggulan": "Context window 200K, safety-focused, coding kuat",
            "biaya": "~$3/1M input tokens, ~$15/1M output tokens",
            "use_case": "Analisis dokumen panjang, coding assistant"
        },
        {
            "nama": "Gemini Pro (Google)",
            "tipe": "CLOSED API",
            "parameter": "Tidak dipublikasi",
            "keunggulan": "Multi-modal native, integrasi Google Cloud",
            "biaya": "Bervariasi per tier",
            "use_case": "Multi-modal AI, integrasi produk Google"
        },
    ]

    open_models = [
        {
            "nama": "Llama 3.1 (Meta)",
            "tipe": "OPEN-SOURCE",
            "parameter": "8B / 70B / 405B",
            "keunggulan": "Performa mendekati GPT-4, lisensi permissive",
            "biaya": "Gratis (butuh GPU)",
            "use_case": "Self-hosted chatbot, fine-tuning custom"
        },
        {
            "nama": "Mistral 7B / Mixtral 8x7B",
            "tipe": "OPEN-SOURCE",
            "parameter": "7B / 46.7B (MoE)",
            "keunggulan": "Efisien, MoE architecture, bahasa Eropa kuat",
            "biaya": "Gratis (butuh GPU)",
            "use_case": "Inference cepat, multilingual tasks"
        },
        {
            "nama": "Gemma 2 (Google)",
            "tipe": "OPEN-SOURCE",
            "parameter": "2B / 9B / 27B",
            "keunggulan": "Ringan, efisien, cocok untuk edge/mobile",
            "biaya": "Gratis (butuh GPU minimal)",
            "use_case": "Edge deployment, perangkat terbatas"
        },
        {
            "nama": "Qwen 2.5 (Alibaba)",
            "tipe": "OPEN-SOURCE",
            "parameter": "0.5B - 72B",
            "keunggulan": "Multilingual kuat, coding bagus, banyak varian",
            "biaya": "Gratis",
            "use_case": "Multilingual, coding, math reasoning"
        },
    ]

    print("\n🔒 MODEL CLOSED / PROPRIETARY API:")
    print("-" * 70)
    for m in closed_models:
        print(f"\n  📌 {m['nama']}")
        print(f"     Parameter  : {m['parameter']}")
        print(f"     Keunggulan : {m['keunggulan']}")
        print(f"     Biaya      : {m['biaya']}")
        print(f"     Use Case   : {m['use_case']}")

    print("\n\n🔓 MODEL OPEN-SOURCE / OPEN-WEIGHT:")
    print("-" * 70)
    for m in open_models:
        print(f"\n  📌 {m['nama']}")
        print(f"     Parameter  : {m['parameter']}")
        print(f"     Keunggulan : {m['keunggulan']}")
        print(f"     Biaya      : {m['biaya']}")
        print(f"     Use Case   : {m['use_case']}")


def faktor_pemilihan_model():
    """Framework untuk memilih model yang tepat."""
    print("\n\n" + "=" * 70)
    print("FRAMEWORK PEMILIHAN MODEL")
    print("=" * 70)

    print("""
    Gunakan checklist ini saat memilih model:

    1. 📋 TASK: Apa yang ingin dicapai?
       - Text generation → GPT-4, Llama, Mistral
       - Image generation → DALL-E, Stable Diffusion
       - Embedding/search → text-embedding-ada-002, BGE, E5
       - Classification → BERT, DistilBERT, DeBERTa

    2. 💰 BUDGET: Berapa anggaran yang tersedia?
       - Tidak ada → Open-source + hardware sendiri
       - Pay-as-you-go → Closed API (bayar per token)
       - Budget besar → Self-hosted open-source di cloud

    3. 🔒 PRIVASI: Apakah data sensitif?
       - Ya → Open-source (self-hosted) atau on-premise
       - Tidak → Closed API bisa dipakai

    4. ⚡ LATENSI: Seberapa cepat response dibutuhkan?
       - Real-time (<100ms) → Model kecil, local deployment
       - Interaktif (<2s) → API atau model medium
       - Batch (tidak urgent) → Model besar, tidak masalah lambat

    5. 🎯 KUALITAS: Seberapa akurat yang dibutuhkan?
       - State-of-the-art → GPT-4, Claude 3.5
       - Cukup baik → Llama 3.1 70B, Mixtral
       - Cukup dasar → Model 7B-13B

    6. 📐 SKALA: Berapa request per hari?
       - <1000/hari → API paling mudah
       - 1000-100K/hari → Pertimbangkan self-hosting
       - >100K/hari → Self-hosting biasanya lebih hemat
    """)


def main():
    bandingkan_model()
    faktor_pemilihan_model()

    print("\n✅ Selesai! Lanjut ke: 2_huggingface_model_hub.py")

if __name__ == "__main__":
    main()
