#!/usr/bin/env python3
"""
02_claude_messages_api.py
Modul eksplorasi Anthropic Claude Messages API:
- Structure Endpoints `/v1/messages`
- System Message Separat & Content Blocks Array
- Multi-block Content (Text + Image + Tool Use)
"""

import json
from typing import Dict, Any, List

def build_claude_messages_payload(prompt: str) -> Dict[str, Any]:
    """Membangun payload resmi Anthropic Messages API."""
    return {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1024,
        "system": [
            {
                "type": "text",
                "text": "Anda adalah pakar keamanan siber enterprise. Berikan jawaban dalam poin-poin teknis.",
                "cache_control": {"type": "ephemeral"} # Prompt Caching Enabled!
            }
        ],
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }

def main():
    print("=" * 65)
    print(" 📜 ANTHROPIC CLAUDE MESSAGES API SPECIFICATION")
    print("=" * 65)
    
    prompt = "Bagaimana cara mencegah serangan SQL Injection pada FastAPI?"
    payload = build_claude_messages_payload(prompt)
    
    print("\n📋 Anthropic API Payload Structure (System Caching + Content Blocks):")
    print(json.dumps(payload, indent=2))
    
    mock_claude_response = {
        "id": "msg_01A2B3C4D5",
        "type": "message",
        "role": "assistant",
        "model": "claude-3-5-sonnet-20241022",
        "content": [
            {
                "type": "text",
                "text": "1. Gunakan ORM seperti SQLAlchemy / SQLModel dengan parameterized queries.\n2. Lakukan validasi skema input ketat menggunakan Pydantic.\n3. Jangan pernah melakukan string concatenation langsung pada query SQL."
            }
        ],
        "usage": {
            "input_tokens": 42,
            "cache_creation_input_tokens": 1200,
            "cache_read_input_tokens": 0,
            "output_tokens": 58
        }
    }
    
    print("\n🤖 Hasil Respons Model:")
    print(mock_claude_response["content"][0]["text"])
    print(f"\n📊 Prompt Cache Stats: {mock_claude_response['usage']['cache_creation_input_tokens']} tokens disiapkan ke cache.")

if __name__ == "__main__":
    main()
