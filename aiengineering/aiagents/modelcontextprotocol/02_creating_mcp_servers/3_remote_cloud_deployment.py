#!/usr/bin/env python3
"""
Modul 02: Creating MCP Servers - Part 3: Remote / Cloud Deployment Mode
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Model Context Protocol Architecture

Skrip ini mendemonstrasikan:
1. Arsitektur Remote / Cloud MCP Server (Hosted over HTTPS/SSE).
2. Mekanisme Otentikasi & Otorisasi (Bearer Token / API Key Header Validation).
3. Manajemen Sesi Multi-Client (Multi-tenant Enterprise Connector).
4. Alur Streaming Response via Server-Sent Events (SSE) & SSE POST Endpoints.
"""

import json
import time
import uuid
from typing import Dict, Any, List

# ANSI Colors
HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

VALID_API_TOKENS = {
    "mcp_secret_token_corp_8899": "Enterprise Admin User",
    "mcp_secret_token_dev_1122": "Developer Sandbox User"
}


class RemoteCloudMCPServerSimulator:
    """
    [ Remote / Cloud MCP Server ]
    Server MCP terpusat yang di-host di Cloud (AWS, GCP, Kubernetes).
    Melayani banyak client secara bersamaan melalui HTTPS + SSE.
    """
    def __init__(self, endpoint_url: str = "https://mcp-gateway.enterprise.com"):
        self.endpoint_url = endpoint_url
        self.active_sessions: Dict[str, Dict[str, Any]] = {}

    def authenticate_request(self, auth_header: str) -> str:
        """Memeriksa apakah Authorization Header valid."""
        if not auth_header or not auth_header.startswith("Bearer "):
            raise PermissionError("Missing or invalid Authorization Header (Format: 'Bearer <token>').")
        
        token = auth_header.split("Bearer ")[1].strip()
        if token not in VALID_API_TOKENS:
            raise PermissionError(f"Unauthorized: Token '{token}' tidak valid atau kedaluwarsa.")
        
        return VALID_API_TOKENS[token]

    def open_sse_connection(self, auth_header: str) -> Dict[str, Any]:
        """Membuka sesi SSE baru untuk client remote."""
        user_identity = self.authenticate_request(auth_header)
        session_id = f"sse_session_{uuid.uuid4().hex[:8]}"
        
        self.active_sessions[session_id] = {
            "user": user_identity,
            "connected_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "post_endpoint": f"{self.endpoint_url}/messages?session_id={session_id}"
        }
        
        print(f"  {GREEN}✓ Otentikasi Berhasil! Identitas: '{user_identity}'{RESET}")
        print(f"  {GREEN}  Sesi SSE Dibuat : {session_id}{RESET}")
        print(f"  {GREEN}  Endpoint POST   : {self.active_sessions[session_id]['post_endpoint']}{RESET}")
        return {"session_id": session_id, "user": user_identity}

    def process_remote_rpc(self, session_id: str, payload_json: str) -> str:
        if session_id not in self.active_sessions:
            return json.dumps({
                "jsonrpc": "2.0",
                "error": {"code": -32000, "message": "Session expired or invalid."}
            })
            
        req = json.loads(payload_json)
        req_id = req.get("id")
        method = req.get("method")
        user = self.active_sessions[session_id]["user"]

        print(f"\n{YELLOW}[Cloud Server Endpoint] Processing POST Request from User '{user}' (Session: {session_id}){RESET}")
        print(f"  Method: '{method}', RPC ID: {req_id}")

        if method == "tools/call" and req.get("params", {}).get("name") == "query_enterprise_sales":
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Cloud DB Query Success for [{user}]: Q2 Revenue = $4.2M (+18% YoY)"
                        }
                    ],
                    "isError": False
                }
            }
        else:
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"status": "Cloud Method Processed", "user": user}
            }
        return json.dumps(response, indent=2)


def main():
    print("=" * 70)
    print(f"{BOLD}{HEADER}DEPLOYMENT MODE 2: REMOTE / CLOUD DEPLOYMENT MODE{RESET}")
    print("Berdasarkan spesifikasi standar Model Context Protocol (HTTPS / SSE Stream)")
    print("=" * 70)

    cloud_server = RemoteCloudMCPServerSimulator()

    # 1. Percobaan Koneksi Tanpa Token (Harus Gagal)
    print(f"\n{BOLD}{CYAN}--- 1. UJI OTENTIKASI: REQUEST TANPA TOKEN (HARUS GAGAL) ---{RESET}")
    try:
        cloud_server.open_sse_connection(auth_header="")
    except PermissionError as e:
        print(f"  {RED}✓ Ditolak Sesuai Ekspektasi: {e}{RESET}")

    # 2. Percobaan Koneksi Dengan Token Valid
    print(f"\n{BOLD}{CYAN}--- 2. UJI OTENTIKASI: REQUEST DENGAN BEARER TOKEN VALID ---{RESET}")
    valid_auth = "Bearer mcp_secret_token_corp_8899"
    sess_info = cloud_server.open_sse_connection(auth_header=valid_auth)
    session_id = sess_info["session_id"]

    # 3. Mengirim Request Remote RPC ke Cloud Endpoint
    print(f"\n{BOLD}{CYAN}--- 3. EKSEKUSI REMOTE RPC TOOL ('query_enterprise_sales') ---{RESET}")
    remote_req = {
        "jsonrpc": "2.0",
        "id": 501,
        "method": "tools/call",
        "params": {
            "name": "query_enterprise_sales",
            "arguments": {"quarter": "Q2-2026"}
        }
    }
    raw_res = cloud_server.process_remote_rpc(session_id, json.dumps(remote_req))
    res = json.loads(raw_res)

    print(f"  {GREEN}Hasil Cloud RPC Response:{RESET}")
    print(f"  --> {res['result']['content'][0]['text']}")

    # 4. Ringkasan Perbandingan Deployment Modes
    print(f"\n{BOLD}{HEADER}=== COMPARISON SUMMARY: LOCAL DESKTOP VS REMOTE CLOUD ==={RESET}")
    print(" 🔹 Local Desktop : Subprocess via Stdio | Zero Latency | Single User | File/CLI Access")
    print(" 🔹 Remote / Cloud : HTTP / SSE Endpoint | Bearer Auth  | Multi-Tenant| SaaS / DB Access")

    print("\n" + "=" * 70)
    print(f"{GREEN}✓ Simulasi Remote / Cloud Deployment Mode Berhasil Selesai!{RESET}")
    print("=" * 70)


if __name__ == "__main__":
    main()
