import os
import json
import time
import uuid
from datetime import datetime

def main():
    print("=== 9.2 Logging dan Tracing (Monitoring Agent) ===\n")
    print("Script ini TIDAK membutuhkan API key.\n")

    # ---------------------------------------------------------------
    # LOGGING & TRACING
    # Mencatat setiap langkah yang dilakukan agent:
    # - Apa yang ditanya user
    # - Tool apa yang dipanggil
    # - Berapa lama setiap langkah
    # - Berapa token yang digunakan
    # - Apakah ada error
    #
    # Penting untuk: debugging, cost tracking, performance monitoring
    # ---------------------------------------------------------------

    # --- IMPLEMENTASI AGENT LOGGER ---
    class AgentLogger:
        """Logger untuk mencatat setiap langkah agent."""

        def __init__(self, session_id=None):
            self.session_id = session_id or str(uuid.uuid4())[:8]
            self.traces = []
            self.start_time = time.time()

        def log_step(self, step_type, data):
            """Mencatat satu langkah agent."""
            entry = {
                "timestamp": datetime.now().isoformat(),
                "elapsed_ms": round((time.time() - self.start_time) * 1000, 2),
                "session_id": self.session_id,
                "step_index": len(self.traces),
                "step_type": step_type,  # "user_input", "llm_call", "tool_call", "response", "error"
                "data": data
            }
            self.traces.append(entry)
            return entry

        def log_user_input(self, user_input):
            return self.log_step("user_input", {"input": user_input})

        def log_llm_call(self, model, messages_count, temperature=None):
            return self.log_step("llm_call", {
                "model": model,
                "messages_count": messages_count,
                "temperature": temperature
            })

        def log_llm_response(self, content_length, token_usage=None, latency_ms=None):
            return self.log_step("llm_response", {
                "content_length": content_length,
                "token_usage": token_usage,
                "latency_ms": latency_ms
            })

        def log_tool_call(self, tool_name, arguments, result=None, latency_ms=None):
            return self.log_step("tool_call", {
                "tool_name": tool_name,
                "arguments": arguments,
                "result_length": len(str(result)) if result else 0,
                "latency_ms": latency_ms
            })

        def log_response(self, final_response):
            return self.log_step("response", {
                "response": final_response[:500]  # Truncate untuk log
            })

        def log_error(self, error_type, message):
            return self.log_step("error", {
                "error_type": error_type,
                "message": message
            })

        def get_summary(self):
            """Mendapatkan ringkasan session."""
            total_time = round((time.time() - self.start_time) * 1000, 2)
            step_types = [t["step_type"] for t in self.traces]

            total_tokens = 0
            total_llm_calls = 0
            total_tool_calls = 0

            for trace in self.traces:
                if trace["step_type"] == "llm_response":
                    usage = trace["data"].get("token_usage", {})
                    total_tokens += usage.get("total_tokens", 0)
                    total_llm_calls += 1
                elif trace["step_type"] == "tool_call":
                    total_tool_calls += 1

            return {
                "session_id": self.session_id,
                "total_steps": len(self.traces),
                "total_time_ms": total_time,
                "total_llm_calls": total_llm_calls,
                "total_tool_calls": total_tool_calls,
                "total_tokens": total_tokens,
                "errors": step_types.count("error"),
                "estimated_cost_usd": round(total_tokens * 0.00000015, 6)  # ~GPT-4o-mini rate
            }

        def print_trace(self):
            """Mencetak trace dalam format yang mudah dibaca."""
            print(f"\n{'═'*60}")
            print(f"📋 TRACE — Session: {self.session_id}")
            print(f"{'═'*60}")

            for trace in self.traces:
                step_type = trace["step_type"]
                elapsed = trace["elapsed_ms"]
                idx = trace["step_index"]

                icons = {
                    "user_input": "👤",
                    "llm_call": "🧠",
                    "llm_response": "💬",
                    "tool_call": "🔧",
                    "response": "✅",
                    "error": "❌"
                }
                icon = icons.get(step_type, "•")

                print(f"\n  [{idx}] {icon} {step_type} (+{elapsed}ms)")

                data = trace["data"]
                for key, value in data.items():
                    val_str = str(value)
                    if len(val_str) > 100:
                        val_str = val_str[:100] + "..."
                    print(f"       {key}: {val_str}")

        def export_jsonl(self, filepath):
            """Export trace ke file JSONL."""
            with open(filepath, 'w') as f:
                for trace in self.traces:
                    f.write(json.dumps(trace, ensure_ascii=False) + "\n")
            return filepath

    # --- SIMULASI AGENT DENGAN LOGGING ---
    print("=" * 60)
    print("SIMULASI: Agent dengan Logging & Tracing")
    print("=" * 60)

    logger = AgentLogger()

    # Simulasi alur agent
    # Step 1: User input
    user_msg = "Cari kontak Budi dan hitung 15% pajak dari Rp 5.000.000"
    logger.log_user_input(user_msg)
    print(f"\n👤 User: {user_msg}")

    # Step 2: LLM Call #1 (routing/planning)
    time.sleep(0.1)  # Simulasi latency
    logger.log_llm_call(model="gpt-4o-mini", messages_count=2, temperature=0.0)
    logger.log_llm_response(
        content_length=150,
        token_usage={"prompt_tokens": 120, "completion_tokens": 30, "total_tokens": 150},
        latency_ms=450
    )
    print("🧠 LLM merespons: Perlu 2 tool calls")

    # Step 3: Tool Call #1
    time.sleep(0.05)
    logger.log_tool_call(
        tool_name="cari_kontak",
        arguments={"nama": "Budi"},
        result='{"nama": "Budi Santoso", "telepon": "081234567890"}',
        latency_ms=15
    )
    print("🔧 Tool: cari_kontak(Budi) → OK")

    # Step 4: Tool Call #2
    time.sleep(0.05)
    logger.log_tool_call(
        tool_name="kalkulator",
        arguments={"ekspresi": "5000000 * 0.15"},
        result='{"hasil": 750000}',
        latency_ms=5
    )
    print("🔧 Tool: kalkulator(5000000 * 0.15) → 750000")

    # Step 5: LLM Call #2 (final response)
    time.sleep(0.1)
    logger.log_llm_call(model="gpt-4o-mini", messages_count=6, temperature=0.5)
    logger.log_llm_response(
        content_length=200,
        token_usage={"prompt_tokens": 250, "completion_tokens": 50, "total_tokens": 300},
        latency_ms=600
    )

    # Step 6: Final response
    final = "Kontak Budi Santoso: 081234567890. Pajak 15% dari Rp 5.000.000 = Rp 750.000."
    logger.log_response(final)
    print(f"✅ Final: {final}")

    # --- PRINT TRACE ---
    logger.print_trace()

    # --- SUMMARY ---
    summary = logger.get_summary()
    print(f"\n{'═'*60}")
    print(f"📊 SESSION SUMMARY")
    print(f"{'═'*60}")
    print(f"  Session ID    : {summary['session_id']}")
    print(f"  Total Steps   : {summary['total_steps']}")
    print(f"  Total Time    : {summary['total_time_ms']}ms")
    print(f"  LLM Calls     : {summary['total_llm_calls']}")
    print(f"  Tool Calls    : {summary['total_tool_calls']}")
    print(f"  Total Tokens  : {summary['total_tokens']}")
    print(f"  Errors        : {summary['errors']}")
    print(f"  Est. Cost     : ${summary['estimated_cost_usd']}")

    # --- EXPORT ---
    export_dir = os.path.dirname(os.path.abspath(__file__))
    export_path = os.path.join(export_dir, "trace_log.jsonl")
    logger.export_jsonl(export_path)
    print(f"\n📁 Trace exported ke: {export_path}")

    # --- DASHBOARD SEDERHANA ---
    print(f"\n{'═'*60}")
    print("📊 CONTOH DASHBOARD MONITORING")
    print(f"{'═'*60}")

    print(f"""
    ┌──────────────────────────────────────────────────────┐
    │                  Agent Dashboard                      │
    ├──────────────────────────────────────────────────────┤
    │  Requests Today    : 1,247                           │
    │  Avg Latency       : 1.2s                            │
    │  Success Rate      : 94.3%                           │
    │  Total Tokens      : 2.1M                            │
    │  Est. Daily Cost   : $0.42                           │
    ├──────────────────────────────────────────────────────┤
    │  Top Tools Used:                                     │
    │    1. kalkulator    (432 calls)                      │
    │    2. cari_kontak   (298 calls)                      │
    │    3. get_waktu     (187 calls)                      │
    ├──────────────────────────────────────────────────────┤
    │  Recent Errors:                                      │
    │    - Tool timeout (3x)                               │
    │    - Rate limit exceeded (1x)                        │
    │    - JSON parse error (2x)                           │
    └──────────────────────────────────────────────────────┘
    """)

    print("✅ Selesai! Memahami logging dan tracing untuk agent.")
    print("\nRingkasan:")
    print("- Log setiap langkah: user input, LLM call, tool call, response, error")
    print("- Track: latency, token usage, cost, success rate")
    print("- Export ke JSONL untuk analisis lanjutan")
    print("- Di produksi, gunakan tools seperti: LangSmith, Langfuse, Phoenix (Arize)")

if __name__ == "__main__":
    main()
