#!/usr/bin/env python3
"""
Modul 6.4: Example Usecase - Web Scraping & Crawling Agent
Simulasi AI Agent yang merayapi (crawling) halaman web, mengekstrak tautan (links),
membersihkan struktur HTML, dan mengumpulkan informasi terarah secara otonom.
"""

import time
import json
from typing import List, Dict, Any

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

class WebScrapingCrawlerAgent:
    def __init__(self):
        self.visited_urls = set()

    def run_agent_loop(self, start_url: str):
        print(f"\n{BOLD}{CYAN}=== USECASE 4: AUTONOMOUS WEB SCRAPING & CRAWLING AGENT ==={RESET}")
        print(f"URL Target Awal: \"{YELLOW}{start_url}{RESET}\"\n")

        steps = [
            ("PERCEPTION", f"Menerima request crawler untuk domain '{start_url}'"),
            ("THOUGHT", f"Iterasi 1: Unduh HTML dari URL awal dan ekstrak meta title & sub-links"),
            ("ACTION", f"call fetch_html(url='{start_url}')"),
            ("OBSERVATION", "HTTP 200 OK. Title: 'AI Agents Roadmap 2026'. Found 2 outbound links: ['/agent-loop', '/tools']"),
            ("THOUGHT", "Iterasi 2: Crawl tautan sekunder '/agent-loop' untuk mengambil informasi spesifik"),
            ("ACTION", "call fetch_html(url='https://roadmap.sh/ai-agents/agent-loop')"),
            ("OBSERVATION", "HTTP 200 OK. Content: 'Agent Loop consists of Perception, Reason, Act, Reflect.'"),
            ("REFLECTION", "Informasi topik Agent Loop berhasil diisolasi dari sitemap. Crawling selesai.")
        ]

        for phase, text in steps:
            if phase == "PERCEPTION":
                print(f"{BOLD}[Perception]{RESET} {text}")
            elif phase == "THOUGHT":
                print(f"  🧠 {BLUE}Thought    :{RESET} {text}")
            elif phase == "ACTION":
                print(f"  ⚡ {YELLOW}Action     :{RESET} {text}")
            elif phase == "OBSERVATION":
                print(f"  👁 {CYAN}Observation:{RESET} {text}")
            elif phase == "REFLECTION":
                print(f"  🏁 {GREEN}Reflection :{RESET} {text}\n")
            time.sleep(0.2)

        print(f"{GREEN}{BOLD}🕸 [HASIL PENGUMPULAN DATA CRAWLING]:{RESET}")
        print(f"  • URL Terjelajahi  : 2 Halaman Web")
        print(f"  • Data Terkstrak   : Topik Agent Loop (4 Pilar Utama)")
        print(f"  • Status Crawling  : {BOLD}SUCCESS / COMPLETED{RESET}\n")

if __name__ == "__main__":
    agent = WebScrapingCrawlerAgent()
    agent.run_agent_loop("https://roadmap.sh/ai-agents")
