#!/usr/bin/env python3
"""
Modul 3.2: Privacy-Preserving Agent Memory
Simulasi pengelolaan memori Agent yang berwawasan privasi:
1. De-identification sebelum penyimpanan memori jangka panjang (Vector DB).
2. TTL (Time-to-Live) Data Retention Policy.
3. Right to be Forgotten (Penghapusan Memori Pengguna).
"""

import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# ANSI Color formatting
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


@dataclass
class MemoryRecord:
    id: str
    user_id: str
    content: str
    timestamp: float
    ttl_seconds: float


class PrivacyMemoryStore:
    """Store Memori Agent berbasis Privasi."""

    def __init__(self):
        self.records: Dict[str, MemoryRecord] = {}

    def add_record(self, record_id: str, user_id: str, content: str, ttl_seconds: float = 5.0):
        # Menyimpan fragmen memori
        now = time.time()
        self.records[record_id] = MemoryRecord(
            id=record_id,
            user_id=user_id,
            content=content,
            timestamp=now,
            ttl_seconds=ttl_seconds
        )
        print(f"{GREEN}[MEMORY ADDED]: Record '{record_id}' disimpan untuk user '{user_id}' (TTL: {ttl_seconds} detik).{RESET}")

    def purge_expired_records(self):
        """TTL Eviction Policy: Menghapus data yang telah melewati masa simpan."""
        now = time.time()
        expired_ids = [
            rec_id for rec_id, rec in self.records.items()
            if (now - rec.timestamp) > rec.ttl_seconds
        ]
        for rec_id in expired_ids:
            del self.records[rec_id]
            print(f"{YELLOW}[TTL EVICTION]: Record '{rec_id}' kadaluarsa dan DIBERSIHKAN dari memori.{RESET}")

    def right_to_be_forgotten(self, user_id: str):
        """GDPR Right to be Forgotten: Menghapus seluruh riwayat memori milik user tertentu."""
        user_rec_ids = [rec_id for rec_id, rec in self.records.items() if rec.user_id == user_id]
        for rec_id in user_rec_ids:
            del self.records[rec_id]
        print(f"{RED}[RIGHT TO BE FORGOTTEN]: Seluruh memori milik user '{user_id}' ({len(user_rec_ids)} record) telah DIHAPUS PERMANEN.{RESET}")

    def get_all_active_memories(self) -> List[MemoryRecord]:
        return list(self.records.values())


def main():
    print(f"\n{BOLD}{CYAN}=== DEMO 3.2: PRIVACY-PRESERVING AGENT MEMORY ==={RESET}\n")

    store = PrivacyMemoryStore()

    # 1. Menambahkan data memori pengguna
    print(f"{BOLD}[1] MENYIMPAN MEMORI DE-IDENTIFIED PENGGUNA{RESET}")
    store.add_record("rec_001", "usr_alice", "User menyukai produk [REDACTED_PRODUCT_A] dan domisili [REDACTED_CITY].", ttl_seconds=2.0)
    store.add_record("rec_002", "usr_alice", "User mengajukan tiket bantuan terkait layanan wifi.", ttl_seconds=10.0)
    store.add_record("rec_003", "usr_bob", "User merekomendasikan fitur ekspor PDF.", ttl_seconds=10.0)
    print()

    print(f"Jumlah memori aktif saat ini: {len(store.get_all_active_memories())}\n")

    # 2. Simulasi Waktu Berjalan untuk TTL Eviction
    print(f"{BOLD}[2] SIMULASI PENATAN ATAU EVICTION KADALUARSA (TTL 2 DETIK PASCA REMOVAL){RESET}")
    print("Menunggu 2.5 detik...")
    time.sleep(2.5)
    store.purge_expired_records()
    print(f"Jumlah memori aktif setelah TTL Purge: {len(store.get_all_active_memories())}\n")

    # 3. Right to be Forgotten (Permintaan Hapus Data User Alice)
    print(f"{BOLD}[3] SIMULASI PERMINTAAN 'RIGHT TO BE FORGOTTEN' (USER ALICE){RESET}")
    store.right_to_be_forgotten("usr_alice")
    print(f"Jumlah memori aktif tersisa: {len(store.get_all_active_memories())}")
    for rec in store.get_all_active_memories():
        print(f"  • Record ID: {rec.id} | User: {rec.user_id} | Content: '{rec.content}'")
    print()

    print(f"{BOLD}{GREEN}✔ Simulasi Modul 3.2 Selesai.{RESET}\n")


if __name__ == "__main__":
    main()
