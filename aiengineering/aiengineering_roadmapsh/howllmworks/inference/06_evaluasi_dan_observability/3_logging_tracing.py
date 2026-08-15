"""
=================================================================
3. LOGGING & TRACING
=================================================================
Logging dan tracing adalah fondasi observability — kemampuan 
untuk memahami APA yang terjadi di dalam sistem.

Logging  = Mencatat event/pesan individual
Tracing  = Melacak alur request dari awal hingga akhir

Mengapa penting untuk AI/inference:
- Debug output model yang aneh/salah
- Lacak chain of API calls (RAG, multi-step)
- Audit trail untuk compliance
- Identifikasi bottleneck performa
=================================================================
"""

import logging
import json
import time
import uuid
from datetime import datetime
from functools import wraps


# ─────────────────────────────────────────────────────
# 1. STRUCTURED LOGGING
# ─────────────────────────────────────────────────────

class InferenceLogger:
    """Logger terstruktur untuk inference pipeline."""

    def __init__(self, service_name="inference-api"):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.DEBUG)

        # Console handler dengan format JSON
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    def _log(self, level, event, **kwargs):
        """Log event dalam format JSON terstruktur."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "service": self.service_name,
            "level": level,
            "event": event,
            **kwargs
        }
        self.logger.log(
            getattr(logging, level.upper()),
            json.dumps(log_entry, ensure_ascii=False)
        )

    def log_request(self, request_id, model, prompt, **kwargs):
        """Log incoming inference request."""
        self._log("INFO", "inference_request",
                  request_id=request_id,
                  model=model,
                  prompt_length=len(prompt),
                  prompt_preview=prompt[:100],
                  **kwargs)

    def log_response(self, request_id, model, output, latency_ms, tokens_used, **kwargs):
        """Log inference response."""
        self._log("INFO", "inference_response",
                  request_id=request_id,
                  model=model,
                  output_length=len(output),
                  output_preview=output[:100],
                  latency_ms=round(latency_ms, 2),
                  tokens_used=tokens_used,
                  **kwargs)

    def log_error(self, request_id, error, **kwargs):
        """Log inference error."""
        self._log("ERROR", "inference_error",
                  request_id=request_id,
                  error_type=type(error).__name__,
                  error_message=str(error),
                  **kwargs)


def demo_structured_logging():
    """Demo structured logging untuk inference."""
    print("=" * 60)
    print("DEMO 1: Structured Logging")
    print("=" * 60)

    logger = InferenceLogger("sentiment-api")

    # Simulasi inference request
    request_id = str(uuid.uuid4())[:8]
    prompt = "Analyze the sentiment of this customer review: This product exceeded my expectations!"

    print(f"\n📝 Simulasi inference request (ID: {request_id}):\n")

    # Log request masuk
    logger.log_request(request_id, "gpt-4o-mini", prompt,
                       endpoint="/predict",
                       user_id="user_123")

    # Simulasi proses
    time.sleep(0.1)

    # Log response
    output = '{"sentiment": "positive", "confidence": 0.95}'
    logger.log_response(request_id, "gpt-4o-mini", output,
                       latency_ms=234.5,
                       tokens_used={"prompt": 25, "completion": 15})

    # Simulasi error
    error_request_id = str(uuid.uuid4())[:8]
    logger.log_error(error_request_id,
                    RuntimeError("Model timeout after 30s"),
                    model="gpt-4o",
                    prompt_length=5000)

    print(f"""
    💡 Keuntungan Structured Logging (JSON):
    - Mudah di-parse oleh tools (ELK, Datadog, CloudWatch)
    - Bisa di-filter dan di-search berdasarkan field
    - Konsisten format antar service
    - Mudah di-aggregate untuk analytics
    """)


# ─────────────────────────────────────────────────────
# 2. REQUEST TRACING
# ─────────────────────────────────────────────────────

class TraceContext:
    """Context manager untuk tracing multi-step inference."""

    def __init__(self, operation_name, trace_id=None, parent_span_id=None):
        self.trace_id = trace_id or str(uuid.uuid4())[:12]
        self.span_id = str(uuid.uuid4())[:8]
        self.parent_span_id = parent_span_id
        self.operation = operation_name
        self.start_time = None
        self.end_time = None
        self.metadata = {}

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        duration_ms = (self.end_time - self.start_time) * 1000
        
        trace_log = {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "operation": self.operation,
            "duration_ms": round(duration_ms, 2),
            "status": "error" if exc_type else "ok",
            **self.metadata
        }
        print(f"   📍 TRACE: {json.dumps(trace_log, ensure_ascii=False)}")

    def set(self, key, value):
        """Tambahkan metadata ke span."""
        self.metadata[key] = value


def demo_request_tracing():
    """Demo tracing untuk RAG (Retrieval-Augmented Generation) pipeline."""
    print("\n" + "=" * 60)
    print("DEMO 2: Request Tracing (RAG Pipeline)")
    print("=" * 60)

    print(f"""
    📋 Skenario: RAG Pipeline (Multi-step)
    
    User Question → Embed → Search Vector DB → Build Prompt → LLM → Response
    
    Setiap langkah perlu di-trace untuk debug & monitoring:
    """)

    trace_id = str(uuid.uuid4())[:12]
    print(f"\n   Trace ID: {trace_id}")
    print(f"   User Query: 'Apa itu quantum computing?'\n")

    # Step 1: Embed query
    with TraceContext("embed_query", trace_id=trace_id) as span:
        span.set("model", "text-embedding-3-small")
        span.set("input_tokens", 8)
        time.sleep(0.05)  # Simulasi

    # Step 2: Search vector DB
    with TraceContext("vector_search", trace_id=trace_id) as span:
        span.set("database", "pinecone")
        span.set("top_k", 5)
        span.set("results_found", 5)
        time.sleep(0.1)  # Simulasi

    # Step 3: Build prompt
    with TraceContext("build_prompt", trace_id=trace_id) as span:
        span.set("template", "rag_v2")
        span.set("context_tokens", 1500)
        span.set("total_prompt_tokens", 1600)
        time.sleep(0.01)  # Simulasi

    # Step 4: LLM inference
    with TraceContext("llm_inference", trace_id=trace_id) as span:
        span.set("model", "gpt-4o-mini")
        span.set("prompt_tokens", 1600)
        span.set("completion_tokens", 250)
        span.set("temperature", 0.3)
        time.sleep(0.3)  # Simulasi

    # Step 5: Post-processing
    with TraceContext("post_process", trace_id=trace_id) as span:
        span.set("citations_added", 3)
        span.set("content_filtered", False)
        time.sleep(0.02)  # Simulasi

    print(f"""
    💡 Dengan tracing, kita bisa:
    - Lihat berapa lama SETIAP langkah memakan waktu
    - Identifikasi bottleneck (langkah mana yang lambat?)
    - Debug error di langkah spesifik
    - Correlate logs dari berbagai service (pakai trace_id)
    """)


def demo_logging_best_practices():
    """Best practices logging untuk inference."""
    print("=" * 60)
    print("DEMO 3: Logging Best Practices")
    print("=" * 60)

    print("""
    ✅ YANG HARUS DI-LOG:
    
    1. 📥 Request:
       - Request ID (untuk korelasi)
       - Model yang dipakai
       - Jumlah token input
       - Preview prompt (50-100 karakter pertama)
       - User ID (jika ada)
    
    2. 📤 Response:
       - Request ID (sama dengan request)
       - Jumlah token output
       - Latensi (ms)
       - Finish reason (stop, length, error)
       - Preview output
    
    3. ❌ Error:
       - Request ID
       - Error type & message
       - Stack trace
       - Model & prompt yang menyebabkan error
    
    4. 💰 Usage:
       - Token count per model per user
       - Cost per request
       - Rate limit hits

    ❌ YANG JANGAN DI-LOG:
    - Full prompt & response (privacy, storage) → log preview saja
    - API keys / secrets
    - PII (Personally Identifiable Information) tanpa masking

    🛠️ TOOLS OBSERVABILITY:
    ┌──────────────────┬────────────────────────────────┐
    │ Tool             │ Kegunaan                       │
    ├──────────────────┼────────────────────────────────┤
    │ LangSmith        │ LLM-specific tracing & eval    │
    │ Helicone         │ OpenAI proxy + analytics       │
    │ Prometheus       │ Metrics collection (open)      │
    │ Grafana          │ Dashboard visualization (open) │
    │ Jaeger/Zipkin    │ Distributed tracing (open)     │
    │ Datadog          │ Full observability (SaaS)      │
    │ OpenTelemetry    │ Standard framework (open)      │
    └──────────────────┴────────────────────────────────┘
    """)


def main():
    demo_structured_logging()
    demo_request_tracing()
    demo_logging_best_practices()

    print("\n" + "=" * 60)
    print("✅ Selesai! Lanjut ke: 07_safety_dan_guardrails/")
    print("=" * 60)

if __name__ == "__main__":
    main()
