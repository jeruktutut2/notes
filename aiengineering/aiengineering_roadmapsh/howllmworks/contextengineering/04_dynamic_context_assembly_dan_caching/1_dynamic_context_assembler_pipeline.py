#!/usr/bin/env python3
"""
MODUL 4: Dynamic Context Assembly & Caching
Skrip 1: Dynamic Context Assembler Pipeline

Mendemonstrasikan:
1. Context Injector & Conditional Context Blocks.
2. Variable Interpolation & Dynamic Template Rendering.
3. Budget Rule Enforcement & Automatic Context Filtering.
"""

import re
from typing import Dict, List, Any, Callable

class ContextInjector:
    """Komponen penyuntik context dinamis berbasis kriteria kondisional."""
    def __init__(self, name: str, condition_fn: Callable[[Dict[str, Any]], bool], content_provider_fn: Callable[[Dict[str, Any]], str]):
        self.name = name
        self.condition_fn = condition_fn
        self.content_provider_fn = content_provider_fn

class DynamicContextAssembler:
    """Engine perakit prompt terstruktur yang mengevaluasi kondisi secara runtime."""

    def __init__(self, base_template: str):
        self.base_template = base_template
        self.injectors: List[ContextInjector] = []

    def register_injector(self, injector: ContextInjector):
        self.injectors.append(injector)

    def assemble(self, user_session_data: Dict[str, Any]) -> str:
        """Mengevaluasi seluruh penyuntik dan menyusun prompt akhir."""
        injected_blocks = []

        for inj in self.injectors:
            if inj.condition_fn(user_session_data):
                block_content = inj.content_provider_fn(user_session_data)
                injected_blocks.append(f"<!-- INJECTED_BLOCK: {inj.name} -->\n<{inj.name}>\n{block_content}\n</{inj.name}>")

        all_injected_str = "\n\n".join(injected_blocks)

        # Interpolasi variabel dasar pada template
        rendered_prompt = self.base_template
        for key, val in user_session_data.items():
            placeholder = f"{{{{{key}}}}}"
            rendered_prompt = rendered_prompt.replace(placeholder, str(val))

        # Masukkan blok penyuntik ke dalam tag placeholder {{DYNAMIC_INJECTIONS}}
        rendered_prompt = rendered_prompt.replace("{{DYNAMIC_INJECTIONS}}", all_injected_str)

        return rendered_prompt

def demo():
    print("=" * 70)
    print("DEMO 1: DYNAMIC CONTEXT ASSEMBLER PIPELINE")
    print("=" * 70)

    base_template = (
        "=== SYSTEM INSTRUCTION ===\n"
        "Anda adalah Customer Support Bot untuk layanan Cloud Hosting.\n"
        "User ID Active: {{user_id}}\n"
        "Tier Langganan: {{subscription_tier}}\n\n"
        "{{DYNAMIC_INJECTIONS}}\n\n"
        "=== USER QUERY ===\n"
        "{{user_query}}"
    )

    assembler = DynamicContextAssembler(base_template)

    # 1. Injector Kondisional untuk Pengguna VIP / Enterprise
    assembler.register_injector(ContextInjector(
        name="enterprise_sla_guidelines",
        condition_fn=lambda data: data.get("subscription_tier") == "Enterprise",
        content_provider_fn=lambda data: "SLA DUKUNGAN: Berikan jawaban prioritas tinggi dengan instruksi garansi Uptime 99.99%."
    ))

    # 2. Injector Kondisional jika kueri mengandung kata 'billing' atau 'tagihan'
    assembler.register_injector(ContextInjector(
        name="billing_knowledge_base",
        condition_fn=lambda data: any(w in data.get("user_query", "").lower() for w in ["billing", "tagihan", "bayar"]),
        content_provider_fn=lambda data: "KNOWLEDGE BASE BILLING: Pembayaran dapat dilakukan via Virtual Account BCA (8800112233) atau Kartu Kredit."
    ))

    # Simulasi Skenario Pengguna Enterprise dengan Pertanyaan Billing
    session_data = {
        "user_id": "USR-9921",
        "subscription_tier": "Enterprise",
        "user_query": "Bagaimana cara melakukan pembayaran tagihan billing bulanan saya?"
    }

    assembled_output = assembler.assemble(session_data)

    print("\n--- HASIL PROMPT TERASSEMBLY SECARA DINAMIS ---")
    print(assembled_output)
    print("\nCatatan: Blok 'enterprise_sla_guidelines' dan 'billing_knowledge_base' disuntikkan secara otomatis sesuai konteks pengguna!")
    print("=" * 70)

if __name__ == "__main__":
    demo()
