#!/usr/bin/env python3
"""
MODUL 5: Context Routing & Multi-Context Orchestration
Skrip 1: Hierarchical Context & Sub-Agent Context Isolation

Mendemonstrasikan:
1. Pembagian Context Hirarkis (Orchestrator Level vs Worker Sub-Agent Level).
2. Minimisasi Pembengkakan Token dengan Hanya Mengirimkan Context Spesifik ke Sub-Agent.
3. Sintesis Kembali Hasil Sub-Agent ke Context Utama.
"""

from typing import Dict, List, Any

class SubAgentContextSlice:
    """Pemotong context terisolasi untuk peran sub-agent tertentu."""

    @staticmethod
    def create_coder_context(global_context: Dict[str, Any], target_file: str) -> str:
        """Context terisolasi khusus agen Coder (hanya butuh spesifikasi fungsi & kode sasaran)."""
        return (
            f"=== ROLE: SOFTWARE CODER SUB-AGENT ===\n"
            f"Target File: {target_file}\n"
            f"Spesifikasi Fungsi: {global_context.get('function_spec')}\n"
            f"Kode Terkait: {global_context.get('existing_code')}\n"
            f"=== TASK: Tuliskan fungsi sesuai spesifikasi. ==="
        )

    @staticmethod
    def create_security_auditor_context(coder_output: str) -> str:
        """Context terisolasi khusus agen Security Auditor (hanya butuh kode yang dihasilkan Coder)."""
        return (
            f"=== ROLE: SECURITY AUDITOR SUB-AGENT ===\n"
            f"Kode yang Perlu Diaudit:\n{coder_output}\n"
            f"=== TASK: Periksa celah keamanan (SQL Injection, XSS, Unsanitized Input). ==="
        )

def demo():
    print("=" * 70)
    print("DEMO 1: HIERARCHICAL CONTEXT & SUB-AGENT ISOLATION")
    print("=" * 70)

    # Global Orchestrator Context (Sangat Besar)
    global_context = {
        "user_request": "Buat fungsi login pengguna di Python.",
        "project_architecture": "Flask REST API + PostgreSQL + JWT Authentication.",
        "function_spec": "def login_user(username, password) -> dict",
        "existing_code": "import jwt\nimport datetime\n\nSECRET_KEY = 'supersecret'",
        "company_docs": "... (5000 kata regulasi perusahaan) ..."
    }

    print("--- [GLOBAL ORCHESTRATOR CONTEXT] ---")
    print(f"Total Ukuran Global Context: ~{sum(len(str(v).split()) for v in global_context.values())} kata.")

    # 1. Slice Context untuk Coder Agent
    coder_context = SubAgentContextSlice.create_coder_context(global_context, target_file="auth/login.py")
    print("\n--- [1. SLICE CONTEXT UNTUK CODER AGENT (TERISOLASI)] ---")
    print(coder_context)
    print(f"Ukuran Token Context Coder: ~{len(coder_context.split())} kata (Menghemat ~90% token dari Global Context!).")

    # Simulasi Output Coder
    coder_output_code = (
        "def login_user(username, password):\n"
        "    if username == 'admin' and password == 'secret':\n"
        "        return {'token': jwt.encode({'user': username}, SECRET_KEY)}\n"
        "    return {'error': 'Invalid credentials'}"
    )

    # 2. Slice Context untuk Security Auditor Agent
    security_context = SubAgentContextSlice.create_security_auditor_context(coder_output_code)
    print("\n--- [2. SLICE CONTEXT UNTUK SECURITY AUDITOR AGENT (TERISOLASI)] ---")
    print(security_context)

    print("\nRingkasan: Dengan Hierarchical Context Isolation, sub-agent tidak dibebani 5000 kata regulasi perusahaan yang tidak relevan!")
    print("=" * 70)

if __name__ == "__main__":
    demo()
