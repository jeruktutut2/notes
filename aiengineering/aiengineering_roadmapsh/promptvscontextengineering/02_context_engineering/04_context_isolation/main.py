#!/usr/bin/env python3
"""
Modul: Context Isolation
Simulasi Multi-Tenant Isolation Boundary dan PII Masking/Redaction Pipeline.
"""

import json
import re

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def sanitize_pii_data(raw_text: str):
    """Masking PII Sensitive Fields"""
    pii_vault = {}
    
    # Phone Masking
    def replace_phone(match):
        token = f"[MASKED_PHONE_{len(pii_vault)+1}]"
        pii_vault[token] = match.group(0)
        return token

    # Email Masking
    def replace_email(match):
        token = f"[MASKED_EMAIL_{len(pii_vault)+1}]"
        pii_vault[token] = match.group(0)
        return token

    sanitized = re.sub(r"\b08\d{8,11}\b", replace_phone, raw_text)
    sanitized = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", replace_email, sanitized)
    
    return sanitized, pii_vault

def main():
    print("=" * 70)
    print(color("  MODUL: CONTEXT ISOLATION & PRIVACY SANITIZATION", "1;34"))
    print("=" * 70)

    raw_user_input = "Nama saya Pak Rian (email: rian.financial@bank.co.id, HP: 081234567890). Mohon verifikasi transaksi deposit saya."
    tenant_id = "TENANT_BANK_SERASI"

    print(color(f"\n1. RAW INPUT FROM USER ({tenant_id}):", "1;33"))
    print(f"\"{raw_user_input}\"")

    sanitized_input, pii_vault = sanitize_pii_data(raw_user_input)

    print(color("\n2. SANITIZED CONTEXT WITH MASKED PII (SENT TO LLM):", "1;32"))
    print(f"\"{sanitized_input}\"")
    print(f"PII Local Vault (Restored Pasca-Response): {json.dumps(pii_vault)}")

    assembled_isolated_prompt = f"""<tenant_isolation_boundary id="{tenant_id}">
CRITICAL PRIVACY RULE: Hanya akses data milik tenant '{tenant_id}'. Dilarang membocorkan data ke tenant lain.
</tenant_isolation_boundary>

<user_sanitized_request>
{sanitized_input}
</user_sanitized_request>"""

    print(color("\n3. ISOLATED CONTEXT WINDOW BOUNDARY:", "1;33"))
    print(assembled_isolated_prompt)

    print("\n" + "=" * 70)
    print("✓ Context Isolation melindungi data pribadi pengguna dan mematuhi aturan kepatuhan GDPR / PDP.")

if __name__ == "__main__":
    main()
