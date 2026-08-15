#!/usr/bin/env python3
"""
Modul 1.1: Perception & User Input Parsing
Demonstrasi bagaimana AI Agent mengorientasikan diri dengan membaca input pengguna,
mengekstrak intent (tujuan), memparsing entitas, dan membangun persepsi awal (Perception State).
"""

import re
import json
from typing import Dict, Any, List
from dataclasses import dataclass, asdict

# ANSI Terminal Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

@dataclass
class PerceptionState:
    raw_input: str
    intent: str
    target_goal: str
    entities: Dict[str, Any]
    input_channel: str
    confidence_score: float

class PerceptionEngine:
    def __init__(self):
        # Database intent sederhana berbasis pola regex untuk simulasi ekstraksi LLM
        self.intent_patterns = [
            (r"(ingat|catat|agenda|jadwal|kegiatan)", "CALENDAR_MANAGEMENT", "Menjadwalkan agenda baru"),
            (r"(buat|tulis|generate|coding|perbaiki|fix|script)", "CODE_GENERATION", "Membuat atau memperbaiki kode program"),
            (r"(analisis|hitung|ringkas|statistik|csv|data)", "DATA_ANALYSIS", "Menganalisis dan mengolah data"),
            (r"(cari|crawl|scrape|web|informasi|artikel)", "WEB_CRAWLING", "Mencari & mengekstrak data dari web"),
            (r"(serang|jalan|buka pintu|musuh|karakter|game)", "GAME_NPC_ACTION", "Menjalankan tindakan NPC dalam game")
        ]

    def parse_input(self, raw_text: str, channel: str = "CLI_TEXT") -> PerceptionState:
        """Memproses input pengguna dan menghasilkan PerceptionState terstruktur."""
        text_lower = raw_text.lower()
        detected_intent = "GENERAL_ASSISTANT"
        target_goal = "Membantu pertanyaan umum pengguna"
        confidence = 0.70

        for pattern, intent, goal in self.intent_patterns:
            if re.search(pattern, text_lower):
                detected_intent = intent
                target_goal = goal
                confidence = 0.95
                break

        # Ekstraksi entitas sederhana (Tanggal, Email, File, Angka)
        entities = {}
        dates = re.findall(r"\b(\d{1,2}\s+[A-Za-z]+|\d{4}-\d{2}-\d{2}|besok|hari ini)\b", raw_text, re.IGNORECASE)
        if dates:
            entities["dates"] = dates

        emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", raw_text)
        if emails:
            entities["emails"] = emails

        filenames = re.findall(r"\b[\w-]+\.(?:py|json|csv|html|txt)\b", raw_text)
        if filenames:
            entities["files"] = filenames

        numbers = re.findall(r"\b\d+\b", raw_text)
        if numbers:
            entities["numbers"] = [int(n) for n in numbers]

        return PerceptionState(
            raw_input=raw_text,
            intent=detected_intent,
            target_goal=target_goal,
            entities=entities,
            input_channel=channel,
            confidence_score=confidence
        )

def main():
    print(f"\n{BOLD}{CYAN}=== MODUL 1.1: PERCEPTION & USER INPUT PARSING ==={RESET}\n")
    engine = PerceptionEngine()

    sample_inputs = [
        "Jadwalkan rapat proyek AI Agents dengan budi@example.com pada 2026-08-01",
        "Tuliskan script Python data.py untuk menganalisis data statistik penjualan",
        "Crawl artikel tentang AI Agents di website https://roadmap.sh/ai-agents",
        "Halo, apa kabar hari ini?"
    ]

    for idx, user_input in enumerate(sample_inputs, 1):
        print(f"{BOLD}Input Contoh #{idx}:{RESET} \"{YELLOW}{user_input}{RESET}\"")
        perception = engine.parse_input(user_input)
        
        print(f"  {BLUE}• Intent Detected :{RESET} {BOLD}{perception.intent}{RESET}")
        print(f"  {BLUE}• Target Goal     :{RESET} {perception.target_goal}")
        print(f"  {BLUE}• Confidence Score:{RESET} {GREEN}{perception.confidence_score * 100:.0f}%{RESET}")
        print(f"  {BLUE}• Extracted Entity:{RESET} {json.dumps(perception.entities, ensure_ascii=False)}")
        print("-" * 65)

if __name__ == "__main__":
    main()
