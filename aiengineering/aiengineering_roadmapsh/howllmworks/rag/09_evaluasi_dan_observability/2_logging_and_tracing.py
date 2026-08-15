import time
import json
import logging

# Inisialisasi Logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class RAGPipelineTracer:
    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self.spans = []
        self.start_time = time.time()

    def add_span(self, name: str, duration_ms: float, metadata: dict = None):
        self.spans.append({
            "span_name": name,
            "duration_ms": round(duration_ms, 2),
            "metadata": metadata or {}
        })

    def summary(self):
        total_duration = round((time.time() - self.start_time) * 1000, 2)
        return {
            "trace_id": self.trace_id,
            "total_duration_ms": total_duration,
            "spans": self.spans
        }

def run_traced_rag_pipeline(query: str):
    tracer = RAGPipelineTracer(trace_id="tr-rag-88421")

    # Step 1: Query Embedding
    t0 = time.time()
    time.sleep(0.02) # Simulasi latensi embedding
    tracer.add_span("Query Embedding", (time.time() - t0) * 1000, {"model": "text-embedding-3-small"})

    # Step 2: Vector Search Retrieval
    t0 = time.time()
    time.sleep(0.04) # Simulasi latensi DB search
    tracer.add_span("Vector DB Search", (time.time() - t0) * 1000, {"top_k": 3, "best_score": 0.88})

    # Step 3: LLM Generation
    t0 = time.time()
    time.sleep(0.15) # Simulasi latensi LLM completion
    tracer.add_span("LLM Answer Generation", (time.time() - t0) * 1000, {"model": "gpt-4o-mini", "prompt_tokens": 250, "completion_tokens": 45})

    return tracer.summary()

def main():
    print("=== 02. Logging & Tracing Pipeline Performance ===")

    query = "Bagaimana arsitektur RAG bekerja?"
    logging.info(f"Mulai mengeksekusi pipeline RAG ter-trace untuk query: '{query}'")

    trace_result = run_traced_rag_pipeline(query)

    print("\n[Ringkasan Execution Trace (JSON)]")
    print(json.dumps(trace_result, indent=2))

    print(f"\n[Analisis Latensi Stage]")
    for span in trace_result["spans"]:
        pct = (span['duration_ms'] / trace_result['total_duration_ms']) * 100
        print(f"  - {span['span_name']:<25}: {span['duration_ms']:>6.2f} ms ({pct:>5.1f}%)")

if __name__ == "__main__":
    main()
