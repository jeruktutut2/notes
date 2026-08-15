#!/usr/bin/env python3
"""
SIMULASI MODUL 4.1: Examples of Tools - Web Search & Database Queries
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Gambar Visual (Tools 1 & 3)

Modul ini mensimulasikan 2 dari 6 kategori tool dasar pada AI Agent:
1. Web Search (Pencarian informasi eksternal real-time)
2. Database Queries (Query SQL terstruktur menggunakan SQLite in-memory)
"""

import sqlite3
import json
import time
from typing import Dict, Any, List

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Mock Web Search Index
WEB_DATABASE = [
    {
        "title": "Perkembangan AI Agents 2026",
        "url": "https://tech-news.id/ai-agents-2026",
        "snippet": "AI Agents kini beralih dari model eksekusi linier ke Tree of Thought dan otonomi multi-agent."
    },
    {
        "title": "Dokumentasi Chain of Thought Reasoning",
        "url": "https://roadmap.sh/ai-agents",
        "snippet": "Chain of Thought memungkinkan LLM memecah masalah matematika dan logika menjadi langkah bertahap."
    },
    {
        "title": "Harga Saham & Pasar Finansial",
        "url": "https://finance-market.id/news",
        "snippet": "Pasar saham teknologi mengalami penguatan menyusul rilis chip AI generasi terbaru."
    }
]

def tool_web_search(query: str, max_results: int = 2) -> Dict[str, Any]:
    print(f"\n{BOLD}{CYAN}[ TOOL EXECUTION: WEB SEARCH ]{RESET}")
    print(f"  🔍 Query: '{query}'")
    time.sleep(0.3)
    
    matched = []
    for item in WEB_DATABASE:
        if any(word.lower() in item["title"].lower() or word.lower() in item["snippet"].lower() for word in query.split()):
            matched.append(item)
            
    matched = matched[:max_results] if matched else WEB_DATABASE[:max_results]
    return {"status": "success", "query": query, "results_count": len(matched), "results": matched}

def tool_database_query(sql_query: str) -> Dict[str, Any]:
    print(f"\n{BOLD}{GREEN}[ TOOL EXECUTION: DATABASE QUERIES (SQL) ]{RESET}")
    print(f"  🗄️ SQL: '{sql_query}'")
    time.sleep(0.3)
    
    # In-Memory SQLite Setup
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    
    # Create sample table & data
    cursor.execute("CREATE TABLE sales (id INT, product TEXT, amount INT, region TEXT)")
    cursor.execute("INSERT INTO sales VALUES (1, 'Laptop AI Pro', 1500, 'Jakarta')")
    cursor.execute("INSERT INTO sales VALUES (2, 'GPU Server Unit', 4500, 'Bandung')")
    cursor.execute("INSERT INTO sales VALUES (3, 'Smart Monitor', 600, 'Jakarta')")
    conn.commit()
    
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        
        result_list = [dict(zip(column_names, row)) for row in rows]
        conn.close()
        return {"status": "success", "rows_found": len(result_list), "data": result_list}
    except Exception as e:
        conn.close()
        return {"status": "error", "error_message": str(e)}

def main():
    print(f"\n{BOLD}{MAGENTA}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}      SIMULASI EXAMPLES OF TOOLS: WEB SEARCH & DATABASE QUERIES        {RESET}")
    print(f"{BOLD}{MAGENTA}======================================================================{RESET}")
    
    # Test Web Search
    search_res = tool_web_search("Chain of Thought AI Agents")
    print(f"{GREEN}Hasil Web Search:{RESET}\n{json.dumps(search_res, indent=4)}")
    
    input(f"\n{YELLOW}Tekan [Enter] untuk menguji Tool Database Query...{RESET}")
    
    # Test DB Query
    db_res = tool_database_query("SELECT product, SUM(amount) as total_sales FROM sales WHERE region = 'Jakarta' GROUP BY product")
    print(f"{GREEN}Hasil DB Query:{RESET}\n{json.dumps(db_res, indent=4)}")
    
    print(f"\n{BOLD}{GREEN}✓ Simulasi Tools Web Search & DB Query Selesai!{RESET}\n")

if __name__ == "__main__":
    main()
