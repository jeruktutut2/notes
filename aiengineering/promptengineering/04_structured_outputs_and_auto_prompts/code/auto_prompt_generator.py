#!/usr/bin/env python3
"""
Modul 04: Automatic Prompt Engineering (APE) Generator
Mengubah draft prompt kasar menjadi Prompt Produksi terstruktur secara otomatis.
"""

def generate_production_prompt(user_draft: str) -> str:
    production_prompt = f"""<system_instruction>
Anda adalah seorang AI Copywriter dan Pakar Pemasaran Digital tingkat atas.
Tugas Anda adalah memproduksi teks promosi penjualan yang persuasif, natural, dan fokus pada manfaat utama produk.
</system_instruction>

<context>
Pengguna ingin mempromosikan produk berikut berdasarkan ide kasar:
"{user_draft}"
</context>

<rules_and_constraints>
1. Gunakan Bahasa Indonesia yang kasual namun tetap profesional dan memikat.
2. Struktur tulisan:
   - Hook menarik di kalimat pertama.
   - 3 Poin Keunggulan Utama (Bullet points dengan emoji).
   - Call to Action (CTA) yang jelas di akhir.
3. Maksimal 150 kata.
4. JANGAN gunakan klaim berlebihan yang tidak masuk akal.
</rules_and_constraints>

<output_format>
Kembalikan jawaban langsung berupa teks promosi tanpa salam pengantar.
</output_format>"""
    return production_prompt

def main():
    print("🪄 AUTOMATIC PROMPT ENGINEERING (APE) DEMO")
    print("=" * 60)
    
    draft_user = "Tolong buatkan deskripsi iklan buat jualan kopi susu gula aren lokal"
    print(f"Draft Kasar Manusia : '{draft_user}'\n")
    
    optimized = generate_production_prompt(draft_user)
    print("--- [PROMPT PRODUKSI HASIL OPTIMASI APE] ---")
    print(optimized)
    print("=" * 60)

if __name__ == "__main__":
    main()
