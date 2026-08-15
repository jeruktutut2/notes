#!/usr/bin/env python3
"""
CLI Runner Interaktif - Model Context Protocol (MCP) Workspace
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Spesifikasi MCP (Anthropic)
"""

import os
import sys
import subprocess

# ANSI Colors
HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


def run_script(script_path: str):
    print(f"\n{'='*70}")
    print(f"Menjalankan: {YELLOW}{os.path.basename(os.path.dirname(script_path))}/{os.path.basename(script_path)}{RESET}")
    print(f"{'='*70}\n")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n{RED}[ERROR] Gagal menjalankan skrip: {e}{RESET}")
    except FileNotFoundError:
        print(f"\n{RED}[ERROR] File tidak ditemukan: {script_path}{RESET}")
    print(f"\n{'='*70}\n")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        print("\n" + "█"*70)
        print(f"{BOLD}{HEADER}=== AI AGENTS: MODEL CONTEXT PROTOCOL (MCP) WORKSPACE ==={RESET}")
        print("█"*70)
        print(f"{CYAN}Berdasarkan Roadmap.sh (AI Agents -> Model Context Protocol & Deployment Modes){RESET}")
        print("Pilih modul / topik pembelajaran yang ingin Anda jalankan:\n")
        
        print(f"{BOLD}[ Modul 1: Core Components ]{RESET}")
        print("  11. MCP Hosts & MCP Client Architecture (Handshake & Discovery)")
        print("  12. MCP Servers & Primitives (Tools, Resources, & Prompts)")
        print("  13. JSON-RPC 2.0 Specification & Transports (Stdio vs SSE)")
        
        print(f"\n{BOLD}[ Modul 2: Creating MCP Servers & Deployment Modes ]{RESET}")
        print("  21. Building MCP Server in Python (SDK Decorator Pattern)")
        print("  22. Deployment Mode 1: Local Desktop (Subprocess Stdio)")
        print("  23. Deployment Mode 2: Remote / Cloud (HTTPS SSE & Bearer Auth)")

        print(f"\n  {BOLD}0. Keluar{RESET}")

        try:
            choice = input(f"\n{YELLOW}Masukkan nomor pilihan (e.g. 11, 12, 21, 22): {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nKeluar dari program.")
            sys.exit(0)

        if choice == '0':
            print("\nTerima kasih telah belajar Model Context Protocol (MCP)!")
            sys.exit(0)

        script_map = {
            '11': os.path.join(base_dir, '01_core_components', '1_mcp_hosts_and_clients.py'),
            '12': os.path.join(base_dir, '01_core_components', '2_mcp_servers_and_primitives.py'),
            '13': os.path.join(base_dir, '01_core_components', '3_jsonrpc_stdio_sse_transports.py'),
            '21': os.path.join(base_dir, '02_creating_mcp_servers', '1_building_mcp_server_python.py'),
            '22': os.path.join(base_dir, '02_creating_mcp_servers', '2_local_desktop_deployment.py'),
            '23': os.path.join(base_dir, '02_creating_mcp_servers', '3_remote_cloud_deployment.py'),
        }

        if choice in script_map:
            run_script(script_map[choice])
        else:
            print(f"\n{RED}Pilihan tidak valid. Silakan coba lagi.{RESET}")


if __name__ == "__main__":
    main()
