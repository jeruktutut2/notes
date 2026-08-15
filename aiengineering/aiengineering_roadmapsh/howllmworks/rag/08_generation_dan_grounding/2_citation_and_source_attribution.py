import os

CITATION_PROMPT = """Jawab pertanyaan berdasarkan konteks di bawah.
Setiap kali Anda menyebutkan fakta, sertakan nomor dokumen referensi dalam kurung siku, contoh: [Dokumen 1].

KONTEKS:
[Dokumen 1] (Sumber: Manual_Python_v2.pdf): Python 3.12 meningkatkan performa interpreter hingga 15%.
[Dokumen 2] (Sumber: Security_Guide.md): Selalu gunakan venv terisolasi untuk menghindari kontaminasi dependency global.

PERTANYAAN: Apa peningkatan di Python 3.12 dan bagaimana praktik keamanan dependency?
"""

def main():
    print("=== 02. Citation & Source Attribution ===")

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key, base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
            resp = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": CITATION_PROMPT}],
                temperature=0.1
            )
            print("Jawaban LLM dengan Sitasi Otomatis:\n")
            print(resp.choices[0].message.content)
            return
        except Exception as e:
            print(f"[WARN] Error API: {e}. Menggunakan output simulasi sitasi.")

    # Fallback simulation
    print("Jawaban LLM dengan Sitasi Otomatis (Simulasi):\n")
    print(
        "Python 3.12 memberikan peningkatan performa interpreter hingga 15% [Dokumen 1]. "
        "Untuk menjaga keamanan dependency, pengembang disarankan selalu menggunakan virtual environment (venv) "
        "terisolasi agar tidak mengkontaminasi package global [Dokumen 2]."
    )

if __name__ == "__main__":
    main()
