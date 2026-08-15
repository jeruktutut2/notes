"""
MODUL 1.2: Persona & Role Prompting
===================================
Penjelasan:
Framing peran (Persona / Role System Prompt) menetapkan ekspektasi pengetahuan,
gaya bahasa, perspektif, dan tingkat detail yang dihasilkan oleh LLM.

Dalam skrip ini, kita membandingkan bagaimana topik teknis yang sama ("Apa itu Latensi vs Throughput?")
dijelaskan oleh 3 persona yang berbeda:
1. Senior Software Architect (Teknis & Presisi)
2. Guru Sekolah Dasar (Analogis & Sederhana)
3. Konsultan Bisnis / Executive (Fokus Dampak ROI & Cost)
"""

def generate_persona_prompt(persona_name: str, system_instruction: str, user_question: str) -> str:
    return f"""[SYSTEM ROLE]: {system_instruction}

[USER QUESTION]: {user_question}

[ASSISTANT RESPONSE]:"""


def simulate_persona_response(persona_id: str, question: str) -> str:
    responses = {
        "architect": (
            "**Perspektif Software Architect:**\n"
            "- **Latensi (Latency):** Waktu tempuh satu unit data dari sender ke receiver (dalam milidetik/ms). Contoh: p99 latency api 50ms.\n"
            "- **Throughput:** Jumlah transaksi/request yang berhasil diproses per satuan waktu (RPS / QPS). Contoh: 10,000 req/sec.\n"
            "-\n Bottleneck latensi tinggi biasanya disebabkan I/O blocking atau network hops, sedangkan throughput terbatas oleh CPU/concurrency bounds."
        ),
        "teacher": (
            "**Perspektif Guru SD:**\n"
            "Bayangkan sebuah jalan tol!\n"
            "- **Latensi** adalah seberapa cepat mobilmu bisa melaju dari gerbang masuk ke gerbang keluar. Semakin cepat, latensinya semakin kecil!\n"
            "- **Throughput** adalah berapa banyak mobil yang bisa keluar dari jalan tol itu dalam waktu 1 menit.\n"
            "Dua-duanya penting supaya jalan tol tidak macet!"
        ),
        "executive": (
            "**Perspektif Konsultan Bisnis / Executive:**\n"
            "- **Latensi** berdampak langsung pada *User Experience (UX)* dan *Conversion Rate*. Pengurangan latensi 100ms meningkatkan revenue hingga 1%.\n"
            "- **Throughput** menentukan *Capacity Limits* dan efisiensi biaya server (Cost per Transaction).\n"
            "Rekomendasi: Prioritaskan optimasi latensi pada checkout flow untuk menekan bounce rate."
        )
    }
    return responses.get(persona_id, "Respon generik.")


def main():
    print("==========================================================")
    print(" DEMO 1.2: Perbandingan Persona & System Role Prompting")
    print("==========================================================\n")

    question = "Jelaskan perbedaan antara Latensi (Latency) dan Throughput!"
    
    personas = [
        ("architect", "Anda adalah Principal Software Architect di perusahaan Fortune 500. Gunakan terminologi teknis presisi."),
        ("teacher", "Anda adalah guru SD yang ramah, analogis, dan pandai menjelaskan hal rumit secara sangat intuitif."),
        ("executive", "Anda adalah CTO / Konsultan Bisnis. Fokus pada dampak finansial, ROI, UX, dan efisiensi biaya.")
    ]

    for p_id, p_sys in personas:
        prompt = generate_persona_prompt(p_id, p_sys, question)
        print(f"=== PERSONA: {p_id.upper()} ===")
        print(f"System Instruction: {p_sys}")
        print("-" * 50)
        print(simulate_persona_response(p_id, question))
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
