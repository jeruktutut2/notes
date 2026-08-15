#!/usr/bin/env python3
"""
Modul: Input Format & Structured Output
Simulasi Input Format XML Delimiters dan JSON Schema Repair Loop.
"""

import json
import re

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def main():
    print("=" * 70)
    print(color("  MODUL: INPUT FORMAT & STRUCTURED OUTPUT", "1;34"))
    print("=" * 70)

    # 1. Input Formatting dengan XML Tags
    print(color("\n1. INPUT FORMATTING USING XML DELIMITERS:", "1;33"))
    raw_prompt = """<instruction>
Ekstrak daftar produk dan harga dari dokumen faktur di bawah.
</instruction>

<invoice_context>
FAKTUR #INV-2026-001
1. Laptop ASUS Zenbook - Qty: 1 - Rp 18.500.000
2. Mouse Wireless Logitech - Qty: 2 - Rp 700.000
</invoice_context>

<output_constraint>
Kembalikan JSON Array: [{"item": str, "qty": int, "total_price": str}]
</output_constraint>"""
    print(raw_prompt)

    # 2. JSON Schema Repair Loop Simulation
    print(color("\n2. STRUCTURED OUTPUT SELF-REPAIR LOOP SIMULATION:", "1;33"))
    malformed_llm_json = """```json
[
  {"item": "Laptop ASUS Zenbook", "qty": 1, "total_price": "Rp 18.500.000"},
  {"item": "Mouse Wireless Logitech", "qty": 2} // missing total_price!
]
```"""
    
    print(color("Raw LLM Output (Rusak / Incomplete):", "31"))
    print(malformed_llm_json)

    # Repair process
    cleaned = re.sub(r"```json\s*|\s*```|//.*", "", malformed_llm_json).strip()
    try:
        parsed = json.loads(cleaned)
        print(color("\nParsing Langsung Selesai:", "32"))
    except json.JSONDecodeError as e:
        print(color(f"\nParsing Gagal: {e}. Menjalankan Repair Loop...", "33"))
        # Simulated repair prompt execution
        repaired_json = [
            {"item": "Laptop ASUS Zenbook", "qty": 1, "total_price": "Rp 18.500.000"},
            {"item": "Mouse Wireless Logitech", "qty": 2, "total_price": "Rp 700.000"}
        ]
        print(color("\nHasil JSON Terperbaiki (Repaired Output):", "1;32"))
        print(json.dumps(repaired_json, indent=2))

    print("\n" + "=" * 70)
    print("✓ Delimiter XML mengisolasi dokumen konteks agar tidak mencemari instruksi utama.")
    print("✓ Self-Repair Loop menjamin keandalan sistem produksi tanpa menghentikan runtime.")

if __name__ == "__main__":
    main()
