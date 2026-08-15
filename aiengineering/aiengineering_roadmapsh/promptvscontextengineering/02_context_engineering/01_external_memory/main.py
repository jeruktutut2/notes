#!/usr/bin/env python3
"""
Modul: External Memory (Context Engineering)
Simulasi External Memory Store (Redis/Vector DB) untuk meng-inject Long-Term State ke Context Window.
"""

import json

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

# Mock External Memory Store (Redis/Database Simulation)
EXTERNAL_MEMORY_STORE = {
    "USR-1092": {
        "name": "Budi Santoso",
        "preferences": {"language": "Indonesian", "risk_appetite": "CONSERVATIVE"},
        "past_portfolio": ["Reksa Dana Pasar Uang", "Obligasi FR0082"],
        "last_interaction": "2026-07-20"
    }
}

def main():
    print("=" * 70)
    print(color("  MODUL: EXTERNAL MEMORY IN CONTEXT ENGINEERING", "1;34"))
    print("=" * 70)

    user_id = "USR-1092"
    user_query = "Rekomendasikan produk investasi tambahan untuk saya bulan ini."

    print(color(f"\n1. FETCHING FROM EXTERNAL MEMORY STORE (User: {user_id}):", "1;33"))
    memory_data = EXTERNAL_MEMORY_STORE.get(user_id)
    print(json.dumps(memory_data, indent=2))

    # Dynamic Injection into Context
    assembled_context = f"""<external_memory_context>
User Profile: {memory_data['name']}
Risk Profile: {memory_data['preferences']['risk_appetite']}
Current Portfolio: {', '.join(memory_data['past_portfolio'])}
</external_memory_context>

<current_user_query>
{user_query}
</current_user_query>"""

    print(color("\n2. ASSEMBLED CONTEXT WINDOW WITH INJECTED EXTERNAL MEMORY:", "1;33"))
    print(assembled_context)

    print(color("\n3. SIMULATED LLM RESPONSE (PERSONALIZED VIA EXTERNAL MEMORY):", "1;32"))
    print(f"Halo Pak {memory_data['name']}, mengingat profil Anda yang konservatif dan portofolio Anda saat ini di Reksa Dana Pasar Uang serta FR0082, "
          "kami merekomendasikan Deposito Syariah atau Sukuk Ritel SR020 yang menawarkan risiko rendah dengan imbal hasil stabil.")

    print("\n" + "=" * 70)
    print("✓ External Memory memungkinkan LLM mengingat konteks jangka panjang pengguna tanpa menyimpan seluruh riwayat di prompt.")

if __name__ == "__main__":
    main()
