#!/usr/bin/env python3
"""
Modul 03: Maintaining Memory
Skrip 2: User Profile Storage (Structured Preferences & Profile Lifecycle)

Simulasi User Profile Storage untuk pemeliharaan profil pengguna.
Fitur utama:
- Struktur profil pengguna JSON/Dict terkonfigurasi.
- Fact Extraction Pipeline (Pembaruan atribut profil dari input pengguna).
- Conflict Resolution (Penanganan pembaruan data yang bertentangan, misal lokasi baru).
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


@dataclass
class UserProfile:
    """Struktur data profil pengguna terstruktur."""
    user_id: str
    name: str
    role: str
    preferences: Dict[str, Any] = field(default_factory=dict)
    history_archive: List[Dict[str, Any]] = field(default_factory=list)

    def update_preference(self, key: str, new_value: Any):
        """Memperbarui preferensi dengan penanganan konflik (Archive data lama jika berubah)."""
        if key in self.preferences and self.preferences[key] != new_value:
            old_value = self.preferences[key]
            self.history_archive.append({
                "key": key,
                "old_value": old_value,
                "new_value": new_value,
                "reason": "User updated preference"
            })
            print(f"{YELLOW}[CONFLICT RESOLUTION]{RESET} Mengubah preferensi '{key}': '{old_value}' -> '{new_value}'. Nilai lama diarsipkan.")
        
        self.preferences[key] = new_value


class UserProfileManager:
    """Manajer Penyimpanan Profil Pengguna."""

    def __init__(self):
        self.profiles: Dict[str, UserProfile] = {}

    def get_or_create_profile(self, user_id: str, name: str, role: str) -> UserProfile:
        if user_id not in self.profiles:
            self.profiles[user_id] = UserProfile(user_id=user_id, name=name, role=role)
        return self.profiles[user_id]

    def extract_facts_from_user_input(self, user_id: str, input_text: str):
        """Aturan simulasi ekstraksi fakta baru dari pesan user."""
        profile = self.profiles.get(user_id)
        if not profile:
            return

        text_lower = input_text.lower()
        if "pindah ke" in text_lower:
            # Ekstraksi lokasi baru
            new_city = input_text.split("pindah ke")[-1].strip().strip(".")
            profile.update_preference("location", new_city.capitalize())
        
        if "suka" in text_lower or "preferensi" in text_lower:
            if "dark mode" in text_lower:
                profile.update_preference("theme", "Dark Mode")
            elif "light mode" in text_lower:
                profile.update_preference("theme", "Light Mode")

        if "bahasa" in text_lower:
            if "inggris" in text_lower or "english" in text_lower:
                profile.update_preference("language", "English")
            elif "indonesia" in text_lower:
                profile.update_preference("language", "Indonesian")


def run_demo():
    print(f"{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}  MODUL 03.2: USER PROFILE STORAGE (STRUCTURED PREFERENCES)          {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    manager = UserProfileManager()

    # 1. Inisialisasi Profil User "usr_101"
    user_id = "usr_101"
    profile = manager.get_or_create_profile(user_id, name="Siti Rahma", role="Software Architect")
    profile.update_preference("location", "Bandung")
    profile.update_preference("theme", "Dark Mode")
    profile.update_preference("language", "Indonesian")

    print(f"{GREEN}[INIT PROFIL]{RESET} Profil Awal Terbuat untuk '{profile.name}':")
    print(json.dumps(asdict(profile), indent=2, ensure_ascii=False))

    # 2. Simulasi Interaksi Pengguna Baru yang Mengubah Data Profil (Conflict Resolution)
    print(f"\n{BOLD}{YELLOW}=== INTERAKSI BARU: PENGGUNA MEMBERIKAN PERNYATAAN KOTA & BAHASA BARU ==={RESET}")
    inputs = [
        "Sekarang saya sudah resmi pindah ke Jakarta.",
        "Tolong respons dengan preferensi bahasa Inggris mulai dari sekarang."
    ]

    for user_input in inputs:
        print(f"\n---> User Input: \"{user_input}\"")
        print("Menjalankan Fact Extraction Pipeline...")
        manager.extract_facts_from_user_input(user_id, user_input)

    # 3. Hasil Profil Terkini Setelah Diperbarui
    print(f"\n{BOLD}{GREEN}=== PROFIL TERBARU USER TERUPDATE DI PROFILE STORE ==={RESET}")
    print(json.dumps(asdict(profile), indent=2, ensure_ascii=False))

    print(f"\n{GREEN}[KESIMPULAN]{RESET} User Profile Storage memastikan preferensi pengguna terus mutakhir dan mengarsipkan konflik historis.")


if __name__ == "__main__":
    run_demo()
