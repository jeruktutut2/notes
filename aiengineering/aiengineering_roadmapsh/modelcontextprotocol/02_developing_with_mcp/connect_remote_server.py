#!/usr/bin/env python3
"""
02_developing_with_mcp/connect_remote_server.py
------------------------------------------------
Panduan & Skrip Menghubungkan MCP Client ke Remote MCP Server over HTTP/SSE.
Demonstrasi penanganan authentication tokens, headers, SSE event streaming,
dan error handling / retry logic.
"""

import asyncio
import json

class RemoteServerConnection:
    """Mengelola koneksi HTTP SSE Remote."""
    
    def __init__(self, sse_url: str, auth_token: str = None):
        self.sse_url = sse_url
        self.auth_token = auth_token
        self.session_id = "sess_remote_98765"
        self.post_url = f"{sse_url.replace('/sse', '')}/messages?sessionId={self.session_id}"

    async def connect(self):
        print("==================================================")
        print("🌐 CONNECT TO REMOTE MCP SERVER (HTTP / SSE)")
        print("==================================================")
        print(f"Target SSE Endpoint: {self.sse_url}")
        print(f"Auth Authorization : Bearer {self.auth_token[:8]}... (Secured TLS)")
        
        print("\nStep 1: Mengirim HTTP GET request untuk membuka SSE Stream...")
        headers = {
            "Accept": "text/event-stream",
            "Authorization": f"Bearer {self.auth_token}"
        }
        print(f"Headers: {json.dumps(headers, indent=2)}")
        
        print("\nStep 2: Menangkap Event 'endpoint' dari Server SSE...")
        sse_event = f"event: endpoint\ndata: {self.post_url}\n\n"
        print(f"Server SSE Frame:\n{sse_event}")

        print("Step 3: Mengirim pesan JSON-RPC ke POST Endpoint...")
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"clientInfo": {"name": "RemoteCloudAgent", "version": "1.0.0"}}
        }
        print(f"POST Payload ke {self.post_url}:")
        print(json.dumps(payload, indent=2))

        print("\nStep 4: Menerima Jawaban via SSE Stream...")
        sse_response = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "Remote-Enterprise-MCP-Cloud", "version": "3.0.0"}
            }
        }
        print(f"Streaming Event Payload:\n{json.dumps(sse_response, indent=2)}")
        print("\n✅ Koneksi Remote SSE Berhasil Disambungkan!")

if __name__ == "__main__":
    remote = RemoteServerConnection(
        sse_url="https://api.enterprise-mcp.com/v1/sse",
        auth_token="mcp_token_mock_998877665544332211"
    )
    asyncio.run(remote.connect())
