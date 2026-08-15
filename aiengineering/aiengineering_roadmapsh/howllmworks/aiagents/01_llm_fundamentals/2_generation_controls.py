import os
from openai import OpenAI

def main():
    print("=== 1.2 Parameter Generasi (Generation Controls) ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        print("Jalankan: export OPENAI_API_KEY='sk-xxx-your-key'")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    prompt = "Sebutkan 3 nama kota di Indonesia."

    # ---------------------------------------------------------------
    # 1. TEMPERATURE
    # Mengontrol tingkat "kreativitas" atau randomness output.
    # - temperature=0.0 → Output sangat deterministik (selalu sama)
    # - temperature=1.0 → Output lebih bervariasi dan kreatif
    # - temperature=2.0 → Output sangat acak (sering tidak koheren)
    # ---------------------------------------------------------------
    print("=" * 60)
    print("1. TEMPERATURE (Kreativitas)")
    print("=" * 60)

    for temp in [0.0, 0.7, 1.5]:
        print(f"\n--- Temperature = {temp} ---")
        # Jalankan 2 kali untuk melihat variasi
        for i in range(2):
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temp,
                max_tokens=100
            )
            jawaban = response.choices[0].message.content.strip()
            print(f"  Percobaan {i+1}: {jawaban}")

    # ---------------------------------------------------------------
    # 2. MAX_TOKENS
    # Membatasi jumlah token maksimal yang dihasilkan oleh LLM.
    # Berguna untuk mengontrol panjang output dan biaya API.
    # ---------------------------------------------------------------
    print("\n" + "=" * 60)
    print("2. MAX_TOKENS (Panjang Output)")
    print("=" * 60)

    prompt_panjang = "Jelaskan tentang sejarah Indonesia secara lengkap."

    for max_tok in [20, 50, 150]:
        print(f"\n--- Max Tokens = {max_tok} ---")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt_panjang}],
            temperature=0.3,
            max_tokens=max_tok
        )
        jawaban = response.choices[0].message.content.strip()
        finish = response.choices[0].finish_reason
        print(f"  Output ({len(jawaban)} karakter): {jawaban}")
        print(f"  Finish Reason: {finish}")
        # 'stop' = selesai normal, 'length' = terpotong karena max_tokens

    # ---------------------------------------------------------------
    # 3. TOP_P (Nucleus Sampling)
    # Alternatif dari temperature. Memilih dari token yang total
    # probabilitasnya mencapai threshold P.
    # - top_p=0.1 → Hanya token paling probable (sangat fokus)
    # - top_p=0.9 → Lebih banyak variasi
    # CATATAN: Biasanya gunakan SALAH SATU (temperature ATAU top_p)
    # ---------------------------------------------------------------
    print("\n" + "=" * 60)
    print("3. TOP_P (Nucleus Sampling)")
    print("=" * 60)

    for top_p in [0.1, 0.5, 0.95]:
        print(f"\n--- Top-P = {top_p} ---")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Buat satu kalimat puitis tentang hujan."}],
            temperature=1.0,  # Biarkan temperature tinggi, variasi dikontrol oleh top_p
            top_p=top_p,
            max_tokens=80
        )
        jawaban = response.choices[0].message.content.strip()
        print(f"  Output: {jawaban}")

    # ---------------------------------------------------------------
    # 4. STOP SEQUENCES
    # Menghentikan generasi saat LLM menghasilkan string tertentu.
    # Berguna untuk memformat output atau menghentikan loop.
    # ---------------------------------------------------------------
    print("\n" + "=" * 60)
    print("4. STOP SEQUENCES (Menghentikan Generasi)")
    print("=" * 60)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Hitung 1 sampai 10, pisahkan dengan koma."}],
        temperature=0.0,
        stop=[",6", ", 6"],  # Berhenti sebelum angka 6
        max_tokens=100
    )
    jawaban = response.choices[0].message.content.strip()
    print(f"  Output (berhenti sebelum 6): {jawaban}")
    print(f"  Finish Reason: {response.choices[0].finish_reason}")

    print("\n✅ Selesai! Eksperimen generation controls berhasil.")
    print("\nRingkasan:")
    print("- Temperature: Kontrol kreativitas (0=deterministik, 1+=kreatif)")
    print("- Max Tokens : Batasi panjang output")
    print("- Top-P      : Alternatif temperature (nucleus sampling)")
    print("- Stop       : Hentikan generasi pada string tertentu")

if __name__ == "__main__":
    main()
