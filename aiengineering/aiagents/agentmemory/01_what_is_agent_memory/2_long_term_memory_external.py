#!/usr/bin/env python3
"""
Modul 01: What is Agent Memory?
Skrip 2: Long-Term Memory (Vector DB / SQL / Custom Persistence)

Simulasi Long-Term Memory (LTM) yang disimpan di database eksternal terisolasi.
Fitur utama:
- Persistensi data antar-sesi percakapan (Cross-Session Persistence).
- Integrasi SQL / Database lokal (SQLite in-memory / persistent file).
- Retrieval terarah dari LTM untuk diinjeksi ke Short-Term Memory saat dibutuhkan.
"""

import sqlite3
import json
import os
from typing import List, Dict, Any

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


class LongTermMemoryDB:
    """Pengelola Long-Term Memory menggunakan SQLite Database Eksternal."""

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        """Membuat tabel memori jangka panjang."""
        query = """
        CREATE TABLE IF NOT EXISTS long_term_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            category TEXT NOT NULL,
            memory_key TEXT NOT NULL,
            memory_value TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def save_memory(self, user_id: str, session_id: str, category: str, key: str, value: str):
        """Menyimpan entri memori jangka panjang secara permanen."""
        query = """
        INSERT INTO long_term_memory (user_id, session_id, category, memory_key, memory_value)
        VALUES (?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (user_id, session_id, category, key, value))
        self.conn.commit()

    def query_memories_by_user(self, user_id: str, category: str = None) -> List[Dict[str, Any]]:
        """Mengambil seluruh memori jangka panjang milik user tertentu."""
        if category:
            query = "SELECT session_id, category, memory_key, memory_value, timestamp FROM long_term_memory WHERE user_id = ? AND category = ?"
            cursor = self.conn.execute(query, (user_id, category))
        else:
            query = "SELECT session_id, category, memory_key, memory_value, timestamp FROM long_term_memory WHERE user_id = ?"
            cursor = self.conn.execute(query, (user_id,))
            
        results = []
        for row in cursor.fetchall():
            results.append({
                "session_id": row[0],
                "category": row[1],
                "key": row[2],
                "value": row[3],
                "timestamp": row[4]
            })
        return results


def run_demo():
    print(f"{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}  MODUL 01.2: LONG-TERM MEMORY (PERSISTENT SQL / EXTERNAL DB)        {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    ltm = LongTermMemoryDB()

    # Sesi 1: Agent berinteraksi dengan user "usr_001" kemarin
    print(f"{BOLD}{GREEN}=== SESI 1 (KEMARIN) - Interaksi Awal & Menyimpan Memori ==={RESET}")
    print("User: 'Saya seorang Data Engineer yang menyukai bahasa Python dan tinggal di Jakarta.'")
    
    ltm.save_memory("usr_001", "sess_101", "user_profile", "job_title", "Data Engineer")
    ltm.save_memory("usr_001", "sess_101", "user_profile", "favorite_language", "Python")
    ltm.save_memory("usr_001", "sess_101", "user_profile", "location", "Jakarta")
    ltm.save_memory("usr_001", "sess_101", "preference", "dark_mode", "True")

    print(f"{GREEN}[SUCCESS]{RESET} Data telah disimpan ke dalam Long-Term Memory (SQLite Storage).\n")

    # Sesi 2: Sesi baru hari ini (Short-Term Memory kosong, tapi Long-Term Memory menyimpan info)
    print(f"{BOLD}{YELLOW}=== SESI 2 (HARI INI - Sesi Baru / Sifat LLM Stateless) ==={RESET}")
    print("Agent memulai sesi baru dengan STM bersih. Membaca Long-Term Memory dari DB untuk User 'usr_001':")

    retrieved_memories = ltm.query_memories_by_user("usr_001")

    print(f"\n{BOLD}[RETRIEVED FROM LONG-TERM MEMORY]{RESET}")
    for mem in retrieved_memories:
        print(f" • [{mem['category'].upper()}] {mem['key']} -> {mem['value']} (Sesi: {mem['session_id']}, Time: {mem['timestamp']})")

    # Rekonstruksi Prompt Sesi 2 dengan suntikan Long-Term Memory
    system_prompt_with_ltm = f"""
=== SYSTEM PROMPT ===
Anda adalah AI Agent Asisten Pribadi.
Berikut adalah informasi Long-Term Memory pengguna yang diambil dari DB:
- Pekerjaan: {next(m['value'] for m in retrieved_memories if m['key'] == 'job_title')}
- Bahasa Favorit: {next(m['value'] for m in retrieved_memories if m['key'] == 'favorite_language')}
- Lokasi: {next(m['value'] for m in retrieved_memories if m['key'] == 'location')}

User Baru Saja Mengatakan: "Rekomendasikan event atau conference yang cocok untuk saya!"
"""
    print(f"\n{BOLD}{CYAN}--- PROMPT HASIL INJEKSI LONG-TERM MEMORY KE SHORT-TERM CONTEXT ---{RESET}")
    print(system_prompt_with_ltm)
    print(f"{GREEN}[KESIMPULAN]{RESET} Long-Term Memory memungkinkan AI Agent mengingat fakta pengguna melintasi sesi berberbeda tanpa batas context window.")


if __name__ == "__main__":
    run_demo()
