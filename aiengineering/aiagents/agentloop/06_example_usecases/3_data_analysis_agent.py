#!/usr/bin/env python3
"""
Modul 6.3: Example Usecase - Data Analysis Agent
Simulasi AI Agent yang bertugas menganalisis dataset tabular (CSV/JSON),
menghitung agregasi statistik, mengekstrak insight tren, dan menyusun ringkasan executive report.
"""

import json
from typing import List, Dict, Any

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

class DataAnalysisAgent:
    def __init__(self):
        # Mock Dataset Penjualan Produk
        self.mock_dataset = [
            {"region": "Jakarta", "category": "Electronics", "revenue": 15000},
            {"region": "Bandung", "category": "Electronics", "revenue": 8000},
            {"region": "Surabaya", "category": "Furniture", "revenue": 12000},
            {"region": "Jakarta", "category": "Furniture", "revenue": 9500},
            {"region": "Medan", "category": "Electronics", "revenue": 11000}
        ]

    def run_agent_loop(self):
        print(f"\n{BOLD}{CYAN}=== USECASE 3: AUTOMATED DATA ANALYSIS AGENT ==={RESET}")
        print(f"Goal: \"Analisis dataset penjualan, cari wilayah dengan revenue tertinggi dan total pendapatan kategori Electronics\"\n")

        steps = [
            ("PERCEPTION", "Membaca dataset sales_q3.csv (5 baris data)"),
            ("THOUGHT", "1. Hitung total revenue berdasarkan wilayah (Region)"),
            ("ACTION", "call group_by_sum(column='region', target='revenue')"),
            ("OBSERVATION", "Jakarta: 24,500 | Surabaya: 12,000 | Medan: 11,000 | Bandung: 8,000"),
            ("THOUGHT", "2. Hitung total revenue khusus untuk kategori 'Electronics'"),
            ("ACTION", "call filter_and_sum(filter_col='category', filter_val='Electronics')"),
            ("OBSERVATION", "Total Revenue Electronics = 34,000 USD (61.2% dari total pendapatan)"),
            ("REFLECTION", "Data teragregasi dengan lengkap. Menyusun Executive Insights Report.")
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

        print(f"{GREEN}{BOLD}📊 [EXECUTIVE DATA ANALYSIS REPORT]:{RESET}")
        print(f"  1. Wilayah Kontributor Tertinggi : {BOLD}Jakarta{RESET} ($24,500 USD)")
        print(f"  2. Kategori Dominan Utamakan    : {BOLD}Electronics{RESET} ($34,000 USD / 61.2%)")
        print(f"  3. Rekomendasi Alokasi Stok    : Tingkatkan persediaan barang elektronik di Jakarta & Medan.\n")

if __name__ == "__main__":
    agent = DataAnalysisAgent()
    agent.run_agent_loop()
