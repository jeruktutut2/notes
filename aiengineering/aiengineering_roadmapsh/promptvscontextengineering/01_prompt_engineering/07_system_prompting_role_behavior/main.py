#!/usr/bin/env python3
"""
Modul: System Prompting, Role & Behavior
Simulasi pengaruh System Persona dan Negative Constraints terhadap perilaku LLM.
"""

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def main():
    print("=" * 70)
    print(color("  MODUL: SYSTEM PROMPTING, ROLE & BEHAVIORAL ALIGNMENT", "1;34"))
    print("=" * 70)

    user_query = "Bagaimana cara membatalkan transaksi yang sudah terlanjur dikirim?"

    # Scenario A: Generic System Prompt
    system_a = "Anda adalah asisten AI."
    
    # Scenario B: Strict Banking Persona + Negative Constraints + Fallback
    system_b = """<system_persona>
Anda adalah Customer Care Officer di Bank Central.
Gunakan Bahasa Indonesia formal, ramah, dan empatik.
</system_persona>

<negative_constraints>
1. DILARANG menjanjikan pengembalian dana instan tanpa verifikasi tim internal.
2. DILARANG meminta PIN atau kata sandi nasabah.
</negative_constraints>

<fallback_instruction>
Jika transaksi sudah berhasil di jaringan antar bank, instruksikan pengguna untuk menghubungi call center di 1500888.
</fallback_instruction>"""

    print(color("\n1. SYSTEM PROMPT GENERIC (TANPA ROLE):", "1;33"))
    print(f"System: '{system_a}'")
    print(color("Hasil Respons: Hubungi pihak bank atau batalkan lewat aplikasi jika ada tombol cancel.", "31"))

    print(color("\n2. SYSTEM PROMPT TERSTRUKTUR (ROLE + CONSTRAINTS):", "1;33"))
    print(system_b)
    print(color("\nHasil Respons Terarah & Aman:", "1;32"))
    print(" Selamat pagi/siang. Mohon maaf atas ketidaknyamanan yang Bapak/Ibu alami. "
          "Sesuai aturan perbankan, transaksi yang telah berhasil diproses melalui jaringan interbank "
          "tidak dapat dibatalkan secara otomatis dari aplikasi. Silakan hubungi Call Center resmi kami di 1500888 "
          "agar petugas kami dapat membantu proses sanggahan transaksi. Demi keamanan, mohon tidak memberikan PIN atau password Anda kepada siapapun.")

    print("\n" + "=" * 70)
    print("✓ System Prompt yang spesifik mencegah halusinasi dan menjamin kepatuhan terhadap aturan bisnis.")

if __name__ == "__main__":
    main()
