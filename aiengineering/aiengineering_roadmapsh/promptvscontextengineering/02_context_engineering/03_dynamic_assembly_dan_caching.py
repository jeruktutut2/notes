#!/usr/bin/env python3
"""
Modul 02: Dynamic Context Assembly, Prefix Caching & Security
Membahas Dynamic Context Assembly Pipeline, Prefix/KV Caching Hit-Miss Simulation, dan PII Sanitizer Multi-Tenant.
"""

import hashlib
import json
import re
import time
from typing import Dict, Any, Tuple

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def print_header(title: str):
    print("\n" + "=" * 70)
    print(color(f"  {title}", "1;34"))
    print("=" * 70)

class DynamicContextAndCaching:
    """Simulasi Pipeline Context Assembler, Caching, dan Sanitasi PII"""

    def __init__(self):
        self.kv_prefix_cache: Dict[str, Dict[str, Any]] = {} # Simulated KV Cache Store

    @staticmethod
    def sanitize_pii(context_text: str) -> Tuple[str, Dict[str, str]]:
        """Mengisolasi dan menyamarkan informasi sensitif (PII) sebelum masuk context"""
        pii_map = {}
        
        # Regex patterns for Email, Phone, Credit Card
        sanitized = context_text
        
        # Email
        emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", sanitized)
        for idx, email in enumerate(emails, 1):
            token = f"[PII_EMAIL_{idx}]"
            pii_map[token] = email
            sanitized = sanitized.replace(email, token)
            
        # Phone
        phones = re.findall(r"\b08\d{8,11}\b", sanitized)
        for idx, phone in enumerate(phones, 1):
            token = f"[PII_PHONE_{idx}]"
            pii_map[token] = phone
            sanitized = sanitized.replace(phone, token)

        return sanitized, pii_map

    def get_or_create_prefix_cache(self, system_instruction_prefix: str) -> Dict[str, Any]:
        """Simulasi Prefix Caching (vLLM / Anthropic Prompt Caching)"""
        prefix_hash = hashlib.sha256(system_instruction_prefix.encode()).hexdigest()[:12]
        
        if prefix_hash in self.kv_prefix_cache:
            entry = self.kv_prefix_cache[prefix_hash]
            entry["hits"] += 1
            return {
                "cache_status": "HIT (0ms TTFT Latency Reduction)",
                "prefix_hash": prefix_hash,
                "cached_tokens": entry["tokens"],
                "saved_cost_percentage": "80% (Cached Read Discount)"
            }
        else:
            token_count = len(system_instruction_prefix.split()) * 1.3 # Rough token estimate
            self.kv_prefix_cache[prefix_hash] = {
                "tokens": int(token_count),
                "created_at": time.time(),
                "hits": 0
            }
            return {
                "cache_status": "MISS (Cold Start - Writing to KV Cache)",
                "prefix_hash": prefix_hash,
                "cached_tokens": int(token_count),
                "saved_cost_percentage": "0% (Full Write Cost)"
            }

    @staticmethod
    def assemble_dynamic_context(
        tenant_id: str,
        user_role: str,
        sanitized_context: str,
        retrieved_knowledge: str
    ) -> str:
        """Dynamic Context Assembler Pipeline"""
        return f"""<!-- TENANT_ISOLATION: {tenant_id} | USER_ROLE: {user_role} -->
<static_system_prefix>
Anda adalah Asisten Virtual resmi {tenant_id}. Dilarang membocorkan data antar tenant.
</static_system_prefix>

<dynamic_knowledge_rag>
{retrieved_knowledge}
</dynamic_knowledge_rag>

<sanitized_user_context>
{sanitized_context}
</sanitized_user_context>"""

def main():
    print_header("MODUL 02: DYNAMIC CONTEXT ASSEMBLY, CACHING & SECURITY")

    # 1. PII Sanitization for Multi-Tenant Context
    print(color("\n1. Sanitasi PII (Privacy Isolation) Sebelum Masuk Context:", "1;33"))
    raw_user_data = "Nama saya Alice. Email saya alice.smith@example.com dan nomor HP 081234567890. Mohon proses refund."
    
    sanitized_text, pii_map = DynamicContextAndCaching.sanitize_pii(raw_user_data)
    print(f"Input Raw Data  : \"{raw_user_data}\"")
    print(color(f"Sanitized Text  : \"{sanitized_text}\"", "1;32"))
    print(f"PII Map Restorer : {json.dumps(pii_map)}")

    # 2. Prefix / Prompt Caching Simulation
    print(color("\n2. Simulasi Prefix / KV Caching (vLLM & LLM Provider Optimization):", "1;33"))
    cache_mgr = DynamicContextAndCaching()
    
    heavy_static_prefix = (
        "System Policy v4.2: Anda adalah bot enterprise perbankan. "
        "Aturan kepatuhan ISO-27001 wajib diterapkan pada setiap transaksi Keuangan. " * 10
    )
    
    print("Request 1 (Pertama kali - Cold Start):")
    res1 = cache_mgr.get_or_create_prefix_cache(heavy_static_prefix)
    print(color(f"  Status: {res1['cache_status']} | Saved Cost: {res1['saved_cost_percentage']}", "31"))
    
    print("\nRequest 2 (Sama Prefix - Warm Cache Hit):")
    res2 = cache_mgr.get_or_create_prefix_cache(heavy_static_prefix)
    print(color(f"  Status: {res2['cache_status']} | Saved Cost: {res2['saved_cost_percentage']}", "32"))

    # 3. Dynamic Context Assembly
    print(color("\n3. Dynamic Context Assembler Pipeline Output:", "1;33"))
    rag_kb = "Kebijakan Refund: Pengembalian dana diproses maksimal 3 hari kerja."
    full_context = DynamicContextAndCaching.assemble_dynamic_context("TENANT_BANK_ABC", "ENTERPRISE_USER", sanitized_text, rag_kb)
    print(color(full_context, "36"))

    print_header("RANGKUMAN DYNAMIC ASSEMBLY & CACHING")
    print("✓ Sanitasi PII mencegah kebocoran informasi sensitif pengguna ke log LLM dan model training.")
    print("✓ Prefix Caching memotong latensi Time-To-First-Token (TTFT) hingga 80% untuk static system prompts.")
    print("✓ Dynamic Context Assembly menggabungkan metadata tenant, RAG, dan user state secara terisolasi.")

if __name__ == "__main__":
    main()
