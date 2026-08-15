#!/usr/bin/env python3
"""
01_core_components/mcp_transports.py
------------------------------------
Demonstrasi dan Pembandingan Lapisan Transpor MCP:
1. Stdio Transport (Standard I/O Subprocess Framing)
2. SSE / HTTP Transport (Server-Sent Events streaming over HTTP)
"""

import asyncio
import json
import sys


class StdioTransportSimulator:
    """
    Simulasi Stdio Transport:
    Menggunakan newline-delimited JSON-RPC framing via stdin/stdout.
    """
    @staticmethod
    def encode_message(msg: dict) -> str:
        """Setiap pesan JSON-RPC di-encode ke JSON string diakhiri newline '\\n'."""
        return json.dumps(msg) + "\n"

    @staticmethod
    def decode_line(line: str) -> dict:
        """Memetakan baris teks kembali ke objek dictionary JSON-RPC."""
        return json.loads(line.strip())


class SSETransportSimulator:
    """
    Simulasi SSE (Server-Sent Events) Transport:
    Memisahkan event stream (Server -> Client) dan HTTP POST (Client -> Server).
    """
    @staticmethod
    def format_sse_event(event_type: str, data: dict) -> str:
        """Membentuk frame W3C SSE event standar."""
        json_str = json.dumps(data)
        return f"event: {event_type}\ndata: {json_str}\n\n"


async def main():
    print("==================================================")
    print("📡 DEMO MCP TRANSPORT LAYER (Stdio vs SSE/HTTP)")
    print("==================================================")

    # 1. Stdio Transport Demo
    print("\n--- 📟 [1] STDIO TRANSPORT (Standard Input/Output) ---")
    print("Karakteristik: Subprocess IPC lokal, latensi terendah, ultra-aman.")
    
    sample_request = {
        "jsonrpc": "2.0",
        "id": 101,
        "method": "tools/list"
    }
    
    encoded_frame = StdioTransportSimulator.encode_message(sample_request)
    print("Framed Stdio Message (dikirim via stdin pipe):")
    print(repr(encoded_frame))
    
    decoded = StdioTransportSimulator.decode_line(encoded_frame)
    print("Parsed Stdio Message (diterima di stdout server):")
    print(json.dumps(decoded, indent=2))

    # 2. SSE Transport Demo
    print("\n--- 🌐 [2] SSE / HTTP TRANSPORT (Server-Sent Events) ---")
    print("Karakteristik: HTTP streaming, remote access, butuh endpoint URL & Port.")
    
    sample_endpoint = "http://localhost:8000/sse"
    session_id = "sess_abc123xyz"
    post_endpoint = f"http://localhost:8000/messages?sessionId={session_id}"
    
    print(f"Saluran GET Event Stream : {sample_endpoint}")
    print(f"Saluran POST Message      : {post_endpoint}")

    event_payload = {
        "jsonrpc": "2.0",
        "method": "notifications/resources/updated",
        "params": {"uri": "file:///logs/system.log"}
    }
    
    sse_frame = SSETransportSimulator.format_sse_event("message", event_payload)
    print("\nFramed SSE Message (Server -> Client Event Stream):")
    print(sse_frame)

    print("\n--- 📊 TABEL PEMBANDING TRANSPORT ---")
    print(f"{'Fitur':<22} | {'Stdio Transport':<25} | {'SSE / HTTP Transport':<25}")
    print("-" * 78)
    print(f"{'Lokasi Server':<22} | {'Mesin Lokal (Subprocess)':<25} | {'Remote / Cloud / Lokal':<25}")
    print(f"{'Mekanisme Komunikasi':<22} | {'stdin / stdout Pipes':<25} | {'HTTP GET SSE + HTTP POST':<25}")
    print(f"{'Kecepatan & Latensi':<22} | {'Sangat Cepat (~0ms)':<25} | {'Tergantung Jaringan Web':<25}")
    print(f"{'Setup Keamanan':<22} | {'Terisolasi di Mesin':<25} | {'Membutuhkan TLS/Bearer Token':<25}")
    print("-" * 78)


if __name__ == "__main__":
    asyncio.run(main())
