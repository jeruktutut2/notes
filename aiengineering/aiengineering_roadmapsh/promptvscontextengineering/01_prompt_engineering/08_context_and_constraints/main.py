#!/usr/bin/env python3
"""
Modul: Context & Constraints
Simulasi Closed-Domain Context Q&A dan Penegakan Hard Constraints.
"""

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def main():
    print("=" * 70)
    print(color("  MODUL: CONTEXT & CONSTRAINTS", "1;34"))
    print("=" * 70)

    context_data = """<context_document>
Jam operasional kantor cabang PT Maju Jaya adalah Hari Senin-Jumat pukul 08:00 - 16:00 WIB.
Layanan Sabtu-Minggu libur. Kuota nomor antrean harian maksimal 100 orang.
</context_document>"""

    query = "Apakah kantor buka hari Sabtu dan jam berapa kuota antrean habis?"

    prompt_with_constraints = f"""{context_data}

<instruction>
Jawab pertanyaan pengguna berdasarkan <context_document> di atas.
</instruction>

<hard_constraints>
1. DILARANG menggunakan pengetahuan di luar <context_document>.
2. Jawab tepat dalam 2 kalimat.
3. Jika informasi tidak ada di konteks, katakan 'Informasi tidak ditemukan dalam dokumen'.
</hard_constraints>

<user_query>
{query}
</user_query>"""

    print(color("\n1. PROMPT DENGAN HARD CONSTRAINTS & CONTEXT:", "1;33"))
    print(prompt_with_constraints)

    print(color("\n2. SIMULASI HASIL RESPONS LLM (TERFOKUS & PATUH):", "1;32"))
    print("Kantor cabang libur pada hari Sabtu dan Minggu. Terkait jam berapa kuota antrean habis, informasi tidak ditemukan dalam dokumen.")

    print("\n" + "=" * 70)
    print("✓ Hard Constraints mencegah LLM berasumsi atau memberikan informasi palsu yang tidak ada di dokumen referensi.")

if __name__ == "__main__":
    main()
