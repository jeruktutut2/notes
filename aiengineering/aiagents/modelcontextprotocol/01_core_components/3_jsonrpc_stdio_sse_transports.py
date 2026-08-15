#!/usr/bin/env python3
"""
Modul 01: Core Components - Part 3: JSON-RPC 2.0 & Transports (Stdio vs SSE)
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Model Context Protocol Specification

Skrip ini mendemonstrasikan:
1. Struktur & Validasi Format JSON-RPC 2.0 (Request, Response, Error).
2. Stdio Transport Mechanism (Standard Input/Output untuk local desktop process IPC).
3. SSE (Server-Sent Events) Transport Mechanism (HTTP Server Streaming untuk Remote Cloud).
"""

import json
import io
import time
from typing import Dict, Any, Generator

# ANSI Colors
HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


class StdioTransportChannel:
    """
    [ Stdio Transport ]
    Transpor berbasis pipa stdin/stdout pada sistem operasi.
    Mengirim baris JSON berselang newline (line-delimited JSON).
    Digunakan untuk Local Desktop Deployment Mode.
    """
    def __init__(self):
        self.pipe_input = io.StringIO()
        self.pipe_output = io.StringIO()

    def send_client_to_server(self, json_message: Dict[str, Any]):
        line = json.dumps(json_message) + "\n"
        print(f"  {YELLOW}[Stdio Out -> stdin Server]: {line.strip()}{RESET}")
        self.pipe_input.write(line)

    def read_server_response(self) -> Dict[str, Any]:
        self.pipe_input.seek(0)
        line = self.pipe_input.readline()
        # Simulasi Server memproses dan menulis ke stdout
        req = json.loads(line)
        response = {
            "jsonrpc": "2.0",
            "id": req.get("id"),
            "result": {"status": "success", "transport": "stdio", "processed_method": req.get("method")}
        }
        resp_line = json.dumps(response) + "\n"
        print(f"  {GREEN}[stdout Server -> Stdio In]: {resp_line.strip()}{RESET}")
        return response


class SSETransportChannel:
    """
    [ SSE Transport (Server-Sent Events over HTTP) ]
    Transpor berbasis HTTP untuk Remote / Cloud Deployment Mode.
    - Client mengirim request via POST request.
    - Server menyiarkan event / respon via HTTP SSE stream (`text/event-stream`).
    """
    def __init__(self, endpoint_url: str = "https://mcp.company.cloud/sse"):
        self.endpoint_url = endpoint_url

    def open_sse_stream(self) -> Generator[str, None, None]:
        print(f"  {CYAN}[HTTP Client] Membuka koneksi GET {self.endpoint_url} (Header: Accept: text/event-stream)...{RESET}")
        events = [
            "event: endpoint\ndata: /messages?session_id=sess_99882233\n\n",
            "event: message\ndata: {\"jsonrpc\":\"2.0\",\"method\":\"notifications/initialized\"}\n\n",
            "event: message\ndata: {\"jsonrpc\":\"2.0\",\"id\":1,\"result\":{\"status\":\"ready_cloud\"}}\n\n"
        ]
        for ev in events:
            time.sleep(0.05)
            yield ev

    def send_http_post_message(self, session_id: str, json_message: Dict[str, Any]):
        post_url = f"{self.endpoint_url}/messages?session_id={session_id}"
        payload = json.dumps(json_message)
        print(f"  {YELLOW}[HTTP POST] Endpoint: {post_url}{RESET}")
        print(f"  {YELLOW}             Payload : {payload}{RESET}")
        return {"status": 202, "message": "Accepted for SSE processing"}


def main():
    print("=" * 70)
    print(f"{BOLD}{HEADER}SIMULASI JSON-RPC 2.0 & TRANSPORT LAYER (STDIO VS SSE){RESET}")
    print("Berdasarkan spesifikasi standar Model Context Protocol (Anthropic/Roadmap.sh)")
    print("=" * 70)

    # ---------------------------------------------------------
    # PART 1: FORMAT PROTOKOL JSON-RPC 2.0
    # ---------------------------------------------------------
    print(f"\n{BOLD}{CYAN}--- 1. SPESIFIKASI STANDAR JSON-RPC 2.0 ---{RESET}")
    
    sample_request = {
        "jsonrpc": "2.0",
        "id": 42,
        "method": "tools/call",
        "params": {"name": "query_db", "arguments": {"sql": "SELECT * FROM users;"}}
    }
    sample_response = {
        "jsonrpc": "2.0",
        "id": 42,
        "result": {"content": [{"type": "text", "text": "Rows returned: 15"}]}
    }
    
    print(f"  {BOLD}Request JSON-RPC 2.0:{RESET}\n{json.dumps(sample_request, indent=4)}")
    print(f"  {BOLD}Response JSON-RPC 2.0:{RESET}\n{json.dumps(sample_response, indent=4)}")

    # ---------------------------------------------------------
    # PART 2: STDIO TRANSPORT (LOCAL DESKTOP MODE)
    # ---------------------------------------------------------
    print(f"\n{BOLD}{CYAN}--- 2. STDIO TRANSPORT MECHANISM (LOCAL DESKTOP) ---{RESET}")
    stdio = StdioTransportChannel()
    print("Mengirim pesan dari MCP Client ke MCP Server via Stdio pipe...")
    stdio.send_client_to_server({"jsonrpc": "2.0", "id": 1, "method": "ping"})
    res_stdio = stdio.read_server_response()
    print(f"  {GREEN}Status Transport Stdio: Latensi ~0ms, Local IPC Ready!{RESET}")

    # ---------------------------------------------------------
    # PART 3: SSE TRANSPORT (REMOTE CLOUD MODE)
    # ---------------------------------------------------------
    print(f"\n{BOLD}{CYAN}--- 3. SSE TRANSPORT MECHANISM (REMOTE CLOUD HTTP) ---{RESET}")
    sse = SSETransportChannel(endpoint_url="https://api.mcp.enterprise.com/sse")
    
    print("Membuka Event Stream SSE dari Cloud Server:")
    session_id = None
    for chunk in sse.open_sse_stream():
        lines = chunk.strip().split('\n')
        for line in lines:
            print(f"    {GREEN}STREAM <- {line}{RESET}")
            if "session_id=" in line:
                session_id = line.split("session_id=")[1]
    
    print(f"\nMengirim pesan RPC balikan via HTTP POST (Session: {session_id}):")
    sse.send_http_post_message(
        session_id=session_id or "sess_99882233",
        json_message={"jsonrpc": "2.0", "id": 100, "method": "tools/call", "params": {"name": "cloud_sync"}}
    )

    print("\n" + "=" * 70)
    print(f"{GREEN}✓ Simulasi Transports (Stdio & SSE) Berhasil Selesai!{RESET}")
    print("=" * 70)


if __name__ == "__main__":
    main()
