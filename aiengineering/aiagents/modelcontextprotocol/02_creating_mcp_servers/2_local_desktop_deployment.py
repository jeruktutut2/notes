#!/usr/bin/env python3
"""
Modul 02: Creating MCP Servers - Part 2: Local Desktop Deployment Mode
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Model Context Protocol Architecture

Skrip ini mendemonstrasikan:
1. Konfigurasi `claude_desktop_config.json` / Host Local Configuration.
2. Peluncuran MCP Server sebagai *Local Subprocess*.
3. Komunikasi IPC (Inter-Process Communication) via `stdio` (`stdin`/`stdout`).
4. Isolasi lokal, keamanan sandbox desktop, dan latensi ~0ms.
"""

import json
import os
import sys
import subprocess
import tempfile
from typing import Dict, Any

# ANSI Colors
HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Contoh Isi File Konfigurasi Host untuk Local Desktop Mode (e.g. `claude_desktop_config.json`)
SAMPLE_HOST_CONFIG = {
    "mcpServers": {
        "sqlite-local-db": {
            "command": "python3",
            "args": ["-c", "import json, sys\nfor line in sys.stdin:\n    req=json.loads(line)\n    print(json.dumps({'jsonrpc':'2.0','id':req['id'],'result':{'status':'Local SQLite Server Active','echo':req.get('method')}}))\n    sys.stdout.flush()\n"],
            "env": {
                "DB_PATH": "/tmp/local_dev.db"
            }
        }
    }
}


class LocalDesktopMCPOrchestrator:
    """
    Simulasi Host Orchestrator yang membaca file `claude_desktop_config.json`
    dan meluncurkan Server MCP lokal sebagai subprocess stdio.
    """
    def __init__(self, config_dict: Dict[str, Any]):
        self.config = config_dict
        self.running_processes: Dict[str, subprocess.Popen] = {}

    def start_local_server(self, server_key: str):
        server_cfg = self.config["mcpServers"].get(server_key)
        if not server_cfg:
            raise ValueError(f"Server key '{server_key}' tidak ditemukan pada konfigurasi Host!")

        command = [server_cfg["command"]] + server_cfg.get("args", [])
        env = os.environ.copy()
        if "env" in server_cfg:
            env.update(server_cfg["env"])

        print(f"{CYAN}[Local Host Launcher] Meluncurkan Subprocess Server '{server_key}'...{RESET}")
        print(f"  Command: {BOLD}{' '.join(command)[:60]}...{RESET}")

        # Launch process with pipes
        proc = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        self.running_processes[server_key] = proc
        print(f"  {GREEN}✓ Subprocess Server Berhasil Dijalankan! PID: {proc.pid}{RESET}")

    def send_request_to_local_server(self, server_key: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        proc = self.running_processes.get(server_key)
        if not proc or proc.poll() is not None:
            raise RuntimeError(f"Server '{server_key}' tidak aktif!")

        payload_line = json.dumps(request_data) + "\n"
        print(f"\n{YELLOW}[Host -> Stdio Subprocess PID {proc.pid}] Sending: {payload_line.strip()}{RESET}")
        
        proc.stdin.write(payload_line)
        proc.stdin.flush()

        response_line = proc.stdout.readline()
        print(f"{GREEN}[Stdio Subprocess PID {proc.pid} -> Host] Received: {response_line.strip()}{RESET}")
        return json.loads(response_line)

    def shutdown(self):
        print(f"\n{CYAN}[Local Host Launcher] Menghentikan seluruh Subprocess MCP Server...{RESET}")
        for server_key, proc in self.running_processes.items():
            if proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=2)
                print(f"  {GREEN}✓ Terminated Server '{server_key}' (PID: {proc.pid}){RESET}")


def main():
    print("=" * 70)
    print(f"{BOLD}{HEADER}DEPLOYMENT MODE 1: LOCAL DESKTOP DEPLOYMENT MODE{RESET}")
    print("Berdasarkan spesifikasi standar Model Context Protocol (Local Stdio Subprocess)")
    print("=" * 70)

    # 1. Menampilkan contoh file konfigurasi Host Desktop
    print(f"\n{BOLD}{CYAN}--- 1. FILE KONFIGURASI HOST DESKTOP (`claude_desktop_config.json`) ---{RESET}")
    print(json.dumps(SAMPLE_HOST_CONFIG, indent=2))

    # 2. Inisialisasi Launcher Subprocess
    orchestrator = LocalDesktopMCPOrchestrator(SAMPLE_HOST_CONFIG)
    
    try:
        # 3. Jalankan Server Lokal
        orchestrator.start_local_server("sqlite-local-db")

        # 4. Kirim Request JSON-RPC 2.0 via Stdio Pipe
        req_init = {"jsonrpc": "2.0", "id": 1, "method": "initialize"}
        res_init = orchestrator.send_request_to_local_server("sqlite-local-db", req_init)
        
        req_list_tools = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
        res_list_tools = orchestrator.send_request_to_local_server("sqlite-local-db", req_list_tools)

    finally:
        # 5. Shutdown rapi
        orchestrator.shutdown()

    print("\n" + "=" * 70)
    print(f"{GREEN}✓ Simulasi Local Desktop Deployment Mode Berhasil Selesai!{RESET}")
    print("=" * 70)


if __name__ == "__main__":
    main()
