#!/usr/bin/env python3
"""
SIMULASI MODUL 4.2: Examples of Tools - Code Execution / REPL & File System Access
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Gambar Visual (Tools 2 & 6)

Modul ini mensimulasikan 2 dari 6 kategori tool dasar pada AI Agent:
1. Code Execution / REPL (Evaluator ekspresi Python / kalkulasi matematika aman)
2. File System Access (Membaca, menulis, dan memeriksa file lokal di workspace sandbox)
"""

import os
import math
import tempfile
import time
import json
from typing import Dict, Any

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

def tool_code_execution_repl(expression: str) -> Dict[str, Any]:
    print(f"\n{BOLD}{CYAN}[ TOOL EXECUTION: CODE EXECUTION / REPL ]{RESET}")
    print(f"  💻 Python Code/Expression: '{expression}'")
    time.sleep(0.3)
    
    # Safe eval context with math library
    safe_globals = {"math": math, "abs": abs, "sum": sum, "max": max, "min": min, "len": len}
    safe_locals = {}
    
    try:
        # Check basic safety
        if "import os" in expression or "import sys" in expression or "subprocess" in expression:
            return {"status": "error", "error_message": "SecurityViolation: Modul sistem tidak diizinkan di REPL sandbox."}
            
        result = eval(expression, safe_globals, safe_locals)
        return {"status": "success", "result": result, "type": type(result).__name__}
    except Exception as e:
        return {"status": "error", "error_message": f"ExecutionError: {e}"}

def tool_file_system_access(action: str, file_path: str, content: str = "") -> Dict[str, Any]:
    print(f"\n{BOLD}{GREEN}[ TOOL EXECUTION: FILE SYSTEM ACCESS ]{RESET}")
    print(f"  📁 Action: '{action}' | Path: '{file_path}'")
    time.sleep(0.3)
    
    try:
        if action == "write":
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"status": "success", "message": f"File berhasil ditulis ke {file_path}", "bytes_written": len(content)}
        elif action == "read":
            if not os.path.exists(file_path):
                return {"status": "error", "error_message": f"FileNotFoundError: File {file_path} tidak ditemukan."}
            with open(file_path, "r", encoding="utf-8") as f:
                data = f.read()
            return {"status": "success", "file_path": file_path, "content": data, "size_bytes": len(data)}
        else:
            return {"status": "error", "error_message": f"Unsupported action '{action}'"}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def main():
    print(f"\n{BOLD}{MAGENTA}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}   SIMULASI EXAMPLES OF TOOLS: CODE EXECUTION / REPL & FILE SYSTEM    {RESET}")
    print(f"{BOLD}{MAGENTA}======================================================================{RESET}")
    
    # Test REPL
    code_expr = "math.sqrt(144) * 10 + sum([1, 2, 3, 4, 5])"
    repl_res = tool_code_execution_repl(code_expr)
    print(f"{GREEN}Hasil REPL Execution:{RESET}\n{json.dumps(repl_res, indent=4)}")
    
    input(f"\n{YELLOW}Tekan [Enter] untuk menguji Tool File System Access...{RESET}")
    
    # Test File System Access using temp file
    temp_dir = os.path.join(tempfile.gettempdir(), "aiagent_sandbox")
    sample_file = os.path.join(temp_dir, "report_summary.txt")
    
    # Write File
    write_res = tool_file_system_access("write", sample_file, "Laporan AI Agent: Chain of Thought & Tool Integration Berhasil Dimuat.")
    print(f"{GREEN}Hasil Write File:{RESET}\n{json.dumps(write_res, indent=4)}")
    
    # Read File
    read_res = tool_file_system_access("read", sample_file)
    print(f"\n{GREEN}Hasil Read File:{RESET}\n{json.dumps(read_res, indent=4)}")
    
    print(f"\n{BOLD}{GREEN}✓ Simulasi Tools Code Execution & File System Selesai!{RESET}\n")

if __name__ == "__main__":
    main()
