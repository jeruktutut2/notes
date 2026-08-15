"""
MODUL 1.1: Anatomi dan Komponen Prompt (Prompt Anatomy & Components)
====================================================================
Penjelasan:
Prompt yang efektif terdiri dari 4 komponen utama:
1. Instruction (Instruksi): Tugas spesifik yang harus dilakukan model.
2. Context (Konteks): Latar belakang atau informasi pendukung untuk membantu model.
3. Input Data (Data Input): Data/teks acuan yang perlu diproses atau dianalisis.
4. Output Indicator (Indikator Output): Format, gaya, atau struktur balasan yang diharapkan.
"""

import json

def generate_prompt(instruction: str, context: str = None, input_data: str = None, output_indicator: str = None) -> str:
    """Menggabungkan komponen-komponen prompt menjadi satu prompt terstruktur."""
    prompt_parts = []
    
    if context:
        prompt_parts.append(f"### KONTEKS:\n{context}")
    
    prompt_parts.append(f"### INSTRUKSI:\n{instruction}")
    
    if input_data:
        prompt_parts.append(f"### DATA INPUT:\n{input_data}")
        
    if output_indicator:
        prompt_parts.append(f"### FORMAT OUTPUT:\n{output_indicator}")
        
    return "\n\n".join(prompt_parts)


def simulate_llm_response(prompt: str) -> str:
    """Simulasi respon LLM berdasarkan kelengkapan komponen prompt."""
    print("--- Prosedur Pemrosesan LLM ---")
    print(f"Menghitung token prompt (~{len(prompt.split())} kata)...")
    
    # Deteksi komponen dalam prompt
    has_context = "### KONTEKS:" in prompt
    has_input = "### DATA INPUT:" in prompt
    has_output_fmt = "### FORMAT OUTPUT:" in prompt
    
    if has_context and has_input and has_output_fmt:
        return json.dumps({
            "status": "Sukses",
            "ringkasan_analisis": "Produk smartphone ini memiliki keunggulan daya tahan baterai 5000mAh dan layar AMOLED 120Hz, namun memiliki kekurangan pada kamera malam yang agak noisy.",
            "sentimen": "Positif dengan Catatan",
            "rekomendasi_tindakan": "Sangat direkomendasikan untuk penggunaan sehari-hari dan gaming ringan."
        }, indent=2, ensure_ascii=False)
    elif has_input:
        return "Produk ini cukup bagus karena baterainya awet 5000mAh, layarnya jernih 120Hz, tapi kameranya kurang oke saat malam hari."
    else:
        return "Saya siap membantu Anda menganalisis produk. Silakan berikan data produknya."


def main():
    print("==========================================================")
    print(" DEMO 1.1: Membedah Anatomi & Komponen Utama Prompt")
    print("==========================================================\n")

    # 1. Contoh Prompt Buruk (Hanya Instruksi Abstrak)
    bad_prompt = "Analisis produk ini."
    print("[1] PROMPT AMBIGU / KRANG SPESIFIK:")
    print("-" * 40)
    print(bad_prompt)
    print("\nRespon LLM:")
    print(simulate_llm_response(bad_prompt))
    print("\n" + "="*60 + "\n")

    # 2. Contoh Prompt Lengkap & Terstruktur (4 Komponen)
    instruction = "Lakukan analisis kelebihan, kekurangan, sentimen, dan berikan rekomendasi pembelian berdasarkan data ulasan produk yang diberikan."
    context = "Anda adalah seorang pakar reviewer gadget senior di Indonesia yang objektif dan berpengalaman selama 10 tahun."
    input_data = (
        "Ulasan Pengguna: 'Saya sudah pakai HP ini selama 2 minggu. Baterai 5000mAh sangat awet, "
        "bisa tahan seharian penuh. Layar AMOLED 120Hz sangat halus. Namun foto di kondisi redup/malam hari "
        "agak banyak noise-nya.'"
    )
    output_indicator = "Berikan jawaban dalam format JSON terstruktur dengan key: status, ringkasan_analisis, sentimen, rekomendasi_tindakan."

    structured_prompt = generate_prompt(instruction, context, input_data, output_indicator)
    
    print("[2] PROMPT TERSTRUKTUR (4 KOMPONEN):")
    print("-" * 40)
    print(structured_prompt)
    print("\nRespon LLM:")
    print(simulate_llm_response(structured_prompt))
    print("\n==========================================================")

if __name__ == "__main__":
    main()
