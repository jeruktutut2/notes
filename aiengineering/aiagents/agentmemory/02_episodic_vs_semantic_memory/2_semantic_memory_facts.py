#!/usr/bin/env python3
"""
Modul 02: Episodic vs Semantic Memory
Skrip 2: Semantic Memory (Factual Knowledge & Entity Stores)

Simulasi Semantic Memory (Memori Semantik / Pengetahuan Faktual).
Fitur utama:
- Ekstraksi dan penyimpanan fakta terstruktur (Entity-Attribute-Value triples / Fact Knowledge Store).
- Terbebas dari konteks waktu spesifik (Time-independent general knowledge).
- Pengabstraksian fakta dari pengalaman mentah menjadi aturan / preferensi permanen.
"""

from typing import List, Dict, Any, Optional

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


class SemanticKnowledgeGraph:
    """Penyimpanan Memori Semantik berbasis Entity-Attribute-Value (EAV)."""

    def __init__(self):
        # Format: {entity: {attribute: value}}
        self.knowledge_base: Dict[str, Dict[str, Any]] = {}

    def upsert_fact(self, entity: str, attribute: str, value: Any, confidence: float = 1.0):
        """Menambah atau memperbarui fakta semantik."""
        if entity not in self.knowledge_base:
            self.knowledge_base[entity] = {}
        
        self.knowledge_base[entity][attribute] = {
            "value": value,
            "confidence": confidence
        }

    def get_fact(self, entity: str, attribute: str) -> Optional[Any]:
        """Mengambil fakta spesifik tentang suatu entitas."""
        if entity in self.knowledge_base and attribute in self.knowledge_base[entity]:
            return self.knowledge_base[entity][attribute]["value"]
        return None

    def get_all_entity_facts(self, entity: str) -> Dict[str, Any]:
        """Mengambil seluruh atribut pengetahuan tentang suatu entitas."""
        if entity not in self.knowledge_base:
            return {}
        return {attr: data["value"] for attr, data in self.knowledge_base[entity].items()}


def run_demo():
    print(f"{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}  MODUL 02.2: SEMANTIC MEMORY (FACTUAL KNOWLEDGE & KNOWLEDGE GRAPH)  {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    semantic_memory = SemanticKnowledgeGraph()

    # Ekstraksi Fakta Semantik dari berbagai interaksi
    print(f"{BOLD}{GREEN}=== INGESTING SEMANTIC FACTS (Ekstraksi Fakta Faktual & Konseptual) ==={RESET}")
    
    # Fakta Entitas User "Budi"
    semantic_memory.upsert_fact("User:Budi", "preferred_language", "Bahasa Indonesia", confidence=0.99)
    semantic_memory.upsert_fact("User:Budi", "coding_style", "PEP8 Python Clean Code", confidence=0.95)
    semantic_memory.upsert_fact("User:Budi", "role", "Lead AI Engineer", confidence=0.90)

    # Fakta Entitas Domain "System_Architecture"
    semantic_memory.upsert_fact("System:Architecture", "database_engine", "PostgreSQL 16", confidence=1.0)
    semantic_memory.upsert_fact("System:Architecture", "mcp_transport", "Stdio Subprocess", confidence=1.0)
    semantic_memory.upsert_fact("System:Architecture", "embedding_dim", 1536, confidence=1.0)

    print(f"{GREEN}[SUCCESS]{RESET} 6 Fakta semantik berhasil disimpan ke dalam Semantic Knowledge Base.\n")

    # Kueri Fakta Semantik oleh Agent
    print(f"{BOLD}{YELLOW}=== AGENT CONSULTING SEMANTIC MEMORY FOR CURRENT QUERY ==={RESET}")
    print("User Pertanyaan: 'Buatkan modul Python sesuai standar coding saya!'")

    user_lang = semantic_memory.get_fact("User:Budi", "preferred_language")
    user_style = semantic_memory.get_fact("User:Budi", "coding_style")
    user_role = semantic_memory.get_fact("User:Budi", "role")

    print(f"\n{BOLD}[RETRIEVED SEMANTIC FACTS FOR 'User:Budi']{RESET}")
    print(f" • Preferred Language : {user_lang}")
    print(f" • Coding Style       : {user_style}")
    print(f" • User Role          : {user_role}")

    db_engine = semantic_memory.get_fact("System:Architecture", "database_engine")
    print(f"\n{BOLD}[RETRIEVED SEMANTIC FACTS FOR 'System:Architecture']{RESET}")
    print(f" • Target Database Engine : {db_engine}")

    print(f"\n{BOLD}{CYAN}--- HASIL SINTESIS DENGAN SEMANTIC MEMORY ---{RESET}")
    print(f"Agent akan menulis kode dalam {user_style}, merespons dalam {user_lang}, dan menggunakan modul {db_engine}.")
    print(f"{GREEN}[KESIMPULAN]{RESET} Semantic Memory menyimpan pengetahuan faktual abstrak yang dapat diakses kapan saja tanpa perlu mencari timestamp kejadian asal.")


if __name__ == "__main__":
    run_demo()
