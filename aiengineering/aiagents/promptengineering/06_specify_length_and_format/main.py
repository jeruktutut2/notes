#!/usr/bin/env python3
"""
Modul 06: Specify Length, Format Etc. & Structured Output Enforcement
----------------------------------------------------------------------
Simulasi pilar keenam Prompt Engineering dari roadmap.sh/ai-agents.
Menunjukkan pentingnya pembatasan panjang keluaran (Word/Token Constraints), pemaksaan format terstruktur (Structured Output Enforcement - JSON/XML Schema),
dan penanganan validasi parsing otomatis untuk AI Agents.
"""

import json
import re
import time
from dataclasses import dataclass
from typing import Dict, Any, Tuple

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"

class StructuredOutputSimulator:
    def __init__(self):
        pass

    def render_header(self):
        print(f"\n{BOLD}{CYAN}=" * 75)
        print(f"{BOLD}{YELLOW}  PILAR 6: SPECIFY LENGTH, FORMAT ETC. & STRUCTURED OUTPUT")
        print(f"{BOLD}{CYAN}=" * 75 + f"{RESET}\n")
        print(f"{GREEN}Prinsip Utama:{RESET} AI Agent membutuhkan output mesin terstruktur (JSON/XML)")
        print(f"tanpa teks conversational agar dapat diparsing langsung secara programmatic.\n")

    def demo_json_schema_enforcement(self):
        print(f"{BOLD}{MAGENTA}[DEMO 1: PEMAKSAAN SKEMA JSON MURNI (STRUCTURED JSON)]{RESET}\n")
        
        prompt_ambiguous = "Ekstrak data pengguna dari teks ini: 'Budi Santoso (30 tahun), Developer di Bandung' ke format JSON."
        prompt_strict = (
            "Anda adalah JSON Extractor Engine.\n"
            "Ekstrak entitas dari teks berikut ke dalam JSON MURNI sesuai JSON Schema berikut:\n"
            "{\n"
            "  \"name\": \"string (Wajib)\",\n"
            "  \"age\": \"integer (Wajib)\",\n"
            "  \"role\": \"string (Wajib)\",\n"
            "  \"location\": \"string (Wajib)\"\n"
            "}\n"
            "ATURAN MUTLAK:\n"
            "1. HANYA hasilkan objek JSON valid.\n"
            "2. DILARANG menyertakan blok kode ```json, kata pengantar, atau penutup."
        )
        
        print(f"{BOLD}{RED}❌ Output Tanpa Enforcement Ketat:{RESET}")
        output_bad = (
            "Tentu! Ini adalah data JSON yang Anda minta:\n\n"
            "```json\n"
            "{\n"
            "  \"nama\": \"Budi Santoso\",\n"
            "  \"umur\": \"30 tahun\",\n"
            "  \"pekerjaan\": \"Developer\"\n"
            "}\n"
            "```\n"
            "Semoga membantu!"
        )
        print(f"{output_bad}\n")
        
        # Uji Parsing JSON
        try:
            json.loads(output_bad)
            print(f"{GREEN}status: Valid JSON Direct Parse{RESET}")
        except Exception as e:
            print(f"{BOLD}{RED}⚠️ ERROR PARSER (json.loads Gagal!):{RESET} {e}")
            print(f"{RED}Alasan: Teks konversasional & tag markdown merusak parser JSON standar.{RESET}\n")

        print(f"{BOLD}{GREEN}✅ Output Dengan Strict Enforcement Prompt:{RESET}")
        output_good = json.dumps({
            "name": "Budi Santoso",
            "age": 30,
            "role": "Developer",
            "location": "Bandung"
        }, indent=2)
        print(f"{output_good}\n")
        
        try:
            parsed = json.loads(output_good)
            print(f"{BOLD}{GREEN}✅ SUCCESS PARSER:{RESET} Berhasil diparsing ke dictionary Python!")
            print(f"   Name: {parsed['name']} | Age: {parsed['age']} | Role: {parsed['role']}\n")
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")

    def demo_length_constraint_validation(self):
        print(f"{BOLD}{CYAN}-" * 75)
        print(f"{BOLD}{MAGENTA}[DEMO 2: VALIDASI BATASAN PANJANG (LENGTH CONSTRAINTS)]{RESET}\n")
        
        target_max_words = 20
        raw_text = (
            "Kecerdasan Buatan (AI) berkembang pesat dengan munculnya Large Language Model "
            "dan arsitektur AI Agent yang mampu mengeksekusi tugas otonom secara terstruktur dan efisien."
        )
        
        prompt_length_constrained = (
            f"Ringkas teks berikut dalam MAX {target_max_words} KATA:\n"
            f"\"{raw_text}\""
        )
        
        simulated_summary = "AI Agent berbasis LLM berkembang pesat untuk mengeksekusi tugas otonom secara efisien dan terstruktur."
        word_count = len(simulated_summary.split())
        
        print(f"{BLUE}Prompt Batasan Panjang:{RESET} \"{prompt_length_constrained}\"")
        print(f"{CYAN}Hasil AI:{RESET} \"{simulated_summary}\"")
        print(f"{BOLD}Jumlah Kata Output:{RESET} {word_count} kata (Target: <= {target_max_words} kata)")
        
        if word_count <= target_max_words:
            print(f"{BOLD}{GREEN}✅ KEPATUHAN PANJANG TERPENUHI!{RESET}\n")
        else:
            print(f"{BOLD}{RED}❌ MELEBIHI BATAS PANJANG!{RESET}\n")

    def demo_robust_extraction_fallback(self):
        print(f"{BOLD}{CYAN}-" * 75)
        print(f"{BOLD}{MAGENTA}[DEMO 3: ROBUST REGEX CLEANER UNTUK OUTPUT AGENT]{RESET}\n")
        print("Jika LLM tetap memuntahkan tag markdown, gunakan Regex Fallback Cleaner:\n")
        
        dirty_llm_output = "```json\n{\"agent_action\": \"SEARCH_WEB\", \"query\": \"prompt engineering roadmap\"}\n```"
        print(f"Dirty Output: {dirty_llm_output}")
        
        # Regex Cleaning
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", dirty_llm_output.strip(), flags=re.IGNORECASE)
        print(f"Cleaned Text: {cleaned}")
        
        data = json.loads(cleaned)
        print(f"{BOLD}{GREEN}Parsed Action Agent:{RESET} {data['agent_action']} -> Query: {data['query']}\n")

def main():
    sim = StructuredOutputSimulator()
    sim.render_header()
    sim.demo_json_schema_enforcement()
    sim.demo_length_constraint_validation()
    sim.demo_robust_extraction_fallback()

if __name__ == "__main__":
    main()
