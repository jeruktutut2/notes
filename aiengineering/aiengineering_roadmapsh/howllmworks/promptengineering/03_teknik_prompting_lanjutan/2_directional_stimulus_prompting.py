"""
MODUL 3.2: Directional Stimulus Prompting
=========================================
Penjelasan:
Directional Stimulus Prompting memberikan petunjuk spesifik (hints / keywords / directional cues)
kepada LLM untuk mengarahkan fokus generasi teks (misalnya agar menekankan aspek tertentu dalam ringkasan).
"""

def generate_directional_prompt(article_text: str, stimulus_keywords: list) -> str:
    hints = ", ".join(stimulus_keywords)
    return f"""Artikel:
"{article_text}"

[DIRECTIONAL HINT]: Fokuskan ringkasan pada aspek berikut: {hints}.

Ringkasan Terarah:"""


def simulate_directional_summary(stimulus_keywords: list) -> str:
    if "keamanan" in stimulus_keywords:
        return "Ringkasan Fokus Keamanan: Sistem operasi baru meluncurkan patch enkripsi 256-bit dan fitur anti-phishing untuk mengamankan data pengguna."
    elif "performa" in stimulus_keywords:
        return "Ringkasan Fokus Performa: Update OS terbaru meningkatkan kecepatan boot 40% dan menghemat konsumsi daya baterai hingga 25%."
    else:
        return "Ringkasan Umum: Update OS baru membawa berbagai perbaikan sistem dan performa."


def main():
    print("==========================================================")
    print(" DEMO 3.2: Directional Stimulus Prompting")
    print("==========================================================\n")

    article = (
        "Perusahaan teknologi X hari ini merilis pembaruan perangkat lunak versi 5.0. "
        "Pembaruan ini menghadirkan sistem enkripsi 256-bit terbaru untuk mencegah kebocoran data. "
        "Selain itu, algoritma baru membuat kecepatan boot 40% lebih cepat dan efisiensi baterai meningkat 25%. "
        "Tampilan antarmuka juga diperbarui menjadi lebih modern."
    )

    print("Artikel Asli:")
    print(article)
    print("\n" + "="*60 + "\n")

    # Skenario 1: Stimulus Keamanan
    hints_sec = ["keamanan", "enkripsi", "kebocoran data"]
    print(f"[1] STIMULUS FOKUS KEAMANAN: {hints_sec}")
    prompt_sec = generate_directional_prompt(article, hints_sec)
    print("Hasil Ringkasan LLM:")
    print(simulate_directional_summary(hints_sec))

    print("\n" + "="*60 + "\n")

    # Skenario 2: Stimulus Performa
    hints_perf = ["performa", "kecepatan boot", "efisiensi baterai"]
    print(f"[2] STIMULUS FOKUS PERFORMA: {hints_perf}")
    prompt_perf = generate_directional_prompt(article, hints_perf)
    print("Hasil Ringkasan LLM:")
    print(simulate_directional_summary(hints_perf))
    print("==========================================================")

if __name__ == "__main__":
    main()
