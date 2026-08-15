"""
MODUL 3.4: Prompt Chaining (Sequential Execution Pipeline)
==========================================================
Penjelasan:
Prompt Chaining adalah teknik menyambungkan beberapa prompt independen menjadi satu alur (pipeline).
Output dari Prompt 1 menjadi Input untuk Prompt 2, dan seterusnya.
Sangat cocok untuk tugas bertahap seperti:
Ekstraksi Data -> Analisis Sentimen -> Pembuatan Draft Balasan Email -> Translasi Bahasa.
"""

import json

def step1_extract_key_info(raw_text: str) -> dict:
    """Prompt 1: Ekstraksi Informasi dari email keluhan."""
    print("Executing Prompt 1: Ekstraksi Informasi...")
    # Simulasi output Prompt 1
    return {
        "nama_pelanggan": "Budi Santoso",
        "produk": "Laptop Gaming X200",
        "keluhan": "Layar flickering setelah update driver",
        "urgensi": "Tinggi"
    }


def step2_generate_action_plan(extracted_data: dict) -> str:
    """Prompt 2: Membuat Rencana Penanganan Teknis."""
    print("Executing Prompt 2: Penentuan Action Plan...")
    return f"Rekomendasikan rollback driver grafis versi 512.15 dan berikan voucher servis gratis untuk {extracted_data['nama_pelanggan']}."


def step3_compose_final_email(extracted_data: dict, action_plan: str, target_language: str = "Indonesian") -> str:
    """Prompt 3: Menyusun Draft Email Resmi."""
    print("Executing Prompt 3: Penyusunan Email Balasan CS...")
    return f"""Yth. Bapak/Ibu {extracted_data['nama_pelanggan']},

Terima kasih telah menghubungi layanan dukungan kami mengenai {extracted_data['produk']}.
Kami memohon maaf atas kendala {extracted_data['keluhan']}.

Langkah Penanganan:
{action_plan}

Hormat kami,
Customer Support Team"""


def main():
    print("==========================================================")
    print(" DEMO 3.4: Prompt Chaining Sequential Pipeline")
    print("==========================================================\n")

    raw_email = (
        "Halo CS, saya Budi Santoso. Laptop Gaming X200 saya layarnya flickering terus "
        "setelah kemarin update driver VGA. Ini sangat mengganggu pekerjaan saya, tolong segera!"
    )

    print(f"Input Raw Text:\n\"{raw_email}\"\n")
    print("-" * 50)

    # Chain Step 1
    extracted_info = step1_extract_key_info(raw_email)
    print(f"Output Prompt 1 (JSON): {json.dumps(extracted_info, ensure_ascii=False)}\n")

    # Chain Step 2
    action_plan = step2_generate_action_plan(extracted_info)
    print(f"Output Prompt 2 (Action Plan): {action_plan}\n")

    # Chain Step 3
    final_email = step3_compose_final_email(extracted_info, action_plan)
    print("Output Prompt 3 (Hasil Akhir Pipeline Email CS):")
    print("-" * 40)
    print(final_email)
    print("==========================================================")

if __name__ == "__main__":
    main()
