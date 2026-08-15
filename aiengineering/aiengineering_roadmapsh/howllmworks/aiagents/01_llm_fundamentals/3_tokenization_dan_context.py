import tiktoken

def main():
    print("=== 1.3 Tokenization dan Context Window ===\n")
    print("Script ini TIDAK membutuhkan API key.\n")

    # ---------------------------------------------------------------
    # 1. APA ITU TOKEN?
    # LLM tidak membaca teks secara langsung. Teks dipecah menjadi
    # "token" — potongan kata/subkata yang memiliki ID numerik.
    # Contoh: "artificial" → ["art", "ificial"] → [472, 82819]
    # ---------------------------------------------------------------
    print("=" * 60)
    print("1. TOKENIZATION - Memecah Teks Menjadi Token")
    print("=" * 60)

    # Menggunakan tiktoken (tokenizer untuk model OpenAI)
    # Encoding yang umum:
    # - "cl100k_base" untuk GPT-4, GPT-3.5-turbo
    # - "o200k_base" untuk GPT-4o, GPT-4o-mini
    encoder = tiktoken.get_encoding("cl100k_base")

    teks_contoh = [
        "Halo, apa kabar?",
        "Artificial Intelligence adalah bidang ilmu komputer.",
        "Indonesia adalah negara kepulauan terbesar di dunia.",
        "🇮🇩 Hello World! 你好世界",
    ]

    for teks in teks_contoh:
        tokens = encoder.encode(teks)
        print(f"\nTeks     : '{teks}'")
        print(f"Token IDs: {tokens}")
        print(f"Jumlah   : {len(tokens)} token")

        # Decode kembali per-token untuk melihat pemecahannya
        pecahan = [encoder.decode([t]) for t in tokens]
        print(f"Pecahan  : {pecahan}")

    # ---------------------------------------------------------------
    # 2. MENGHITUNG JUMLAH TOKEN
    # Penting untuk memperkirakan biaya API dan memastikan prompt
    # tidak melebihi context window.
    # ---------------------------------------------------------------
    print("\n" + "=" * 60)
    print("2. MENGHITUNG TOKEN - Estimasi Biaya dan Kapasitas")
    print("=" * 60)

    teks_panjang = """
    AI Agent adalah sistem yang menggunakan Large Language Model (LLM) sebagai otak
    untuk membuat keputusan, berinteraksi dengan tools eksternal, dan menyelesaikan
    tugas secara otonom. Berbeda dengan chatbot biasa yang hanya menjawab pertanyaan,
    AI Agent bisa merencanakan langkah-langkah, mengeksekusi aksi, dan belajar dari
    hasilnya dalam sebuah loop yang berkelanjutan.
    """

    tokens_panjang = encoder.encode(teks_panjang)
    print(f"\nTeks ({len(teks_panjang)} karakter):")
    print(f"  Jumlah token: {len(tokens_panjang)}")

    # Estimasi biaya (contoh harga GPT-4o-mini)
    harga_per_1m_input = 0.15   # USD per 1M input tokens
    harga_per_1m_output = 0.60  # USD per 1M output tokens
    biaya_input = (len(tokens_panjang) / 1_000_000) * harga_per_1m_input
    print(f"  Estimasi biaya input: ${biaya_input:.8f} (GPT-4o-mini)")

    # ---------------------------------------------------------------
    # 3. CONTEXT WINDOW
    # Setiap model punya batas maksimal token yang bisa diproses
    # dalam satu request (input + output gabungan).
    # ---------------------------------------------------------------
    print("\n" + "=" * 60)
    print("3. CONTEXT WINDOW - Batas Kapasitas Model")
    print("=" * 60)

    context_windows = {
        "GPT-4o-mini":     128_000,
        "GPT-4o":          128_000,
        "GPT-3.5-turbo":   16_385,
        "Claude 3.5 Sonnet": 200_000,
        "Llama 3.1 8B":    128_000,
        "Gemma 2":         8_192,
    }

    print(f"\n{'Model':<22} {'Context Window':>15} {'~Setara Kata':>15}")
    print("-" * 55)
    for model_name, window in context_windows.items():
        # Rata-rata 1 token ≈ 0.75 kata dalam bahasa Inggris
        kata_approx = int(window * 0.75)
        print(f"{model_name:<22} {window:>15,} {kata_approx:>15,}")

    # ---------------------------------------------------------------
    # 4. SIMULASI: Apakah Prompt Muat di Context Window?
    # ---------------------------------------------------------------
    print("\n" + "=" * 60)
    print("4. SIMULASI - Cek Apakah Prompt Muat di Context Window")
    print("=" * 60)

    # Simulasi system prompt + user prompt + cadangan untuk output
    system_prompt = "Kamu adalah asisten AI yang membantu pengguna. Jawab dalam Bahasa Indonesia."
    user_prompt = "Jelaskan tentang AI Agent secara detail." + (" Berikan penjelasan yang sangat panjang." * 100)

    token_system = len(encoder.encode(system_prompt))
    token_user = len(encoder.encode(user_prompt))
    total_input = token_system + token_user
    max_output = 4096  # cadangan untuk output
    context_window = 128_000  # GPT-4o

    print(f"\n  Token System Prompt : {token_system:,}")
    print(f"  Token User Prompt   : {token_user:,}")
    print(f"  Total Input         : {total_input:,}")
    print(f"  Cadangan Output     : {max_output:,}")
    print(f"  Total Dibutuhkan    : {total_input + max_output:,}")
    print(f"  Context Window      : {context_window:,}")

    sisa = context_window - total_input - max_output
    if sisa > 0:
        print(f"  ✅ MUAT! Sisa ruang  : {sisa:,} token")
    else:
        print(f"  ❌ TIDAK MUAT! Kelebihan: {abs(sisa):,} token")
        print(f"  💡 Solusi: Potong prompt, atau gunakan model dengan context window lebih besar.")

    # ---------------------------------------------------------------
    # 5. PERBANDINGAN ENCODING
    # Model berbeda menggunakan tokenizer berbeda
    # ---------------------------------------------------------------
    print("\n" + "=" * 60)
    print("5. PERBANDINGAN TOKENIZER")
    print("=" * 60)

    teks_test = "Saya sedang belajar membuat AI Agent menggunakan Python."

    encodings = {
        "cl100k_base (GPT-4/3.5)": tiktoken.get_encoding("cl100k_base"),
        "o200k_base (GPT-4o)": tiktoken.get_encoding("o200k_base"),
    }

    print(f"\nTeks: '{teks_test}'\n")
    for nama, enc in encodings.items():
        tokens = enc.encode(teks_test)
        print(f"  {nama}:")
        print(f"    Jumlah token: {len(tokens)}")
        print(f"    Token IDs   : {tokens}")
        pecahan = [enc.decode([t]) for t in tokens]
        print(f"    Pecahan     : {pecahan}\n")

    print("✅ Selesai! Sekarang Anda memahami bagaimana tokenization bekerja.")
    print("\nRingkasan:")
    print("- Token = unit terkecil yang dipahami LLM (bukan karakter, bukan kata)")
    print("- Jumlah token menentukan biaya API dan batas context window")
    print("- Tokenizer berbeda menghasilkan pecahan token yang berbeda")
    print("- Selalu hitung token sebelum mengirim prompt besar ke API")

if __name__ == "__main__":
    main()
