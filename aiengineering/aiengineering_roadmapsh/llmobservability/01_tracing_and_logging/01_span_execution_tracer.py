"""
01_span_execution_tracer.py
---------------------------
Lab runnable untuk mendemonstrasikan pohon eksekusi Tracing & Logging (Trace -> Span -> Event)
sesuai dengan prinsip OpenTelemetry / OpenInference pada LLM.
"""

import time
import json
import uuid
from typing import List, Dict, Any, Optional

class Event:
    def __init__(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        self.timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.name = name
        self.attributes = attributes or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "name": self.name,
            "attributes": self.attributes
        }

class Span:
    def __init__(self, name: str, span_type: str = "GENERIC", parent_id: Optional[str] = None):
        self.span_id = f"span-{uuid.uuid4().hex[:6]}"
        self.parent_id = parent_id
        self.name = name
        self.span_type = span_type
        self.start_time = None
        self.end_time = None
        self.duration_ms = 0.0
        self.attributes = {}
        self.events = []
        self.children = []

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.duration_ms = round((self.end_time - self.start_time) * 1000, 2)

    def set_attribute(self, key: str, value: Any):
        self.attributes[key] = value

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        self.events.append(Event(name, attributes))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "span_id": self.span_id,
            "parent_id": self.parent_id,
            "name": self.name,
            "span_type": self.span_type,
            "duration_ms": self.duration_ms,
            "attributes": self.attributes,
            "events": [e.to_dict() for e in self.events],
            "children": [c.to_dict() for c in self.children]
        }

class Trace:
    def __init__(self, name: str):
        self.trace_id = f"tr-{uuid.uuid4().hex[:8]}"
        self.name = name
        self.root_spans: List[Span] = []

    def print_tree(self, span: Span = None, depth: int = 0):
        spans_to_print = [span] if span else self.root_spans
        indent = "  " * depth
        prefix = "└── " if depth > 0 else "📌 "

        for s in spans_to_print:
            print(f"{indent}{prefix}[{s.span_type}] {s.name} ({s.duration_ms}ms) [ID: {s.span_id}]")
            for k, v in s.attributes.items():
                print(f"{indent}    🔹 {k}: {v}")
            for ev in s.events:
                print(f"{indent}    ⚡ Event: {ev.name} ({ev.attributes})")
            for child in s.children:
                self.print_tree(child, depth + 1)


# Simulation function representing a RAG pipeline execution
def run_rag_simulation():
    print(f"\n=======================================================")
    print(f"🚀 MENJALANKAN SIMULASI TRACING: RAG PIPELINE EXECUTION")
    print(f"=======================================================\n")

    trace = Trace("RAG Customer Support Assistant")

    # Root Span: Agent Execution
    with Span("RAG Pipeline Workflow", span_type="CHAIN") as root:
        trace.root_spans.append(root)
        root.set_attribute("user.id", "user_1084")
        root.set_attribute("session.id", "sess_9921")

        # Step 1: Vector DB Search
        with Span("Vector Retrieval (ChromaDB)", span_type="RETRIEVER", parent_id=root.span_id) as search_span:
            root.children.append(search_span)
            search_span.set_attribute("db.vector_store", "Chroma")
            search_span.set_attribute("retrieval.top_k", 3)
            time.sleep(0.12)  # Simulate DB latency
            search_span.add_event("Chunks Retrieved", {"doc_ids": ["doc_12", "doc_88"], "similarity_score": 0.89})

        # Step 2: Prompt Construction
        with Span("Construct Prompt", span_type="PROMPT", parent_id=root.span_id) as prompt_span:
            root.children.append(prompt_span)
            prompt_span.set_attribute("prompt.template_id", "tpl_qa_v2")
            prompt_span.set_attribute("prompt.system", "You are a helpful customer support AI.")
            time.sleep(0.04)

        # Step 3: LLM Inference
        with Span("LLM Inference (GPT-4o)", span_type="LLM", parent_id=root.span_id) as llm_span:
            root.children.append(llm_span)
            llm_span.set_attribute("llm.model_name", "gpt-4o")
            llm_span.set_attribute("llm.temperature", 0.3)
            llm_span.set_attribute("llm.tokens.prompt", 852)
            time.sleep(0.25)  # Simulate generation latency
            llm_span.add_event("TTFT Received", {"ttft_ms": 140})
            llm_span.set_attribute("llm.tokens.completion", 145)
            llm_span.set_attribute("llm.tokens.total", 997)

    # Print Trace Hierarchy
    print(f"Trace ID: {trace.trace_id} - Name: {trace.name}")
    print("-" * 60)
    trace.print_tree()
    print("-" * 60)

    print("\n✅ Trace data berhasil dibuat dan terstruktur!")

if __name__ == "__main__":
    run_rag_simulation()
