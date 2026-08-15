"""
server.py
---------
FastAPI HTTP Backend Server untuk LLM Observability Web Visualizer.
"""

import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, List

app = FastAPI(title="LLM Observability Web Visualizer API")

# Pricing data reference
PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
}

class CostRequest(BaseModel):
    model: str
    prompt_tokens: int
    completion_tokens: int

class EvalRequest(BaseModel):
    query: str
    context: str
    response: str

@app.get("/api/health")
def health_check():
    return {"status": "online", "module": "LLM Observability"}

@app.post("/api/calculate-cost")
def calculate_cost(req: CostRequest):
    if req.model not in PRICING:
        raise HTTPException(status_code=400, detail="Model tidak didukung.")
    
    p_rate = PRICING[req.model]["input"]
    c_rate = PRICING[req.model]["output"]
    
    input_cost = (req.prompt_tokens / 1_000_000) * p_rate
    output_cost = (req.completion_tokens / 1_000_000) * c_rate
    total_cost = input_cost + output_cost

    return {
        "model": req.model,
        "prompt_tokens": req.prompt_tokens,
        "completion_tokens": req.completion_tokens,
        "input_cost_usd": round(input_cost, 6),
        "output_cost_usd": round(output_cost, 6),
        "total_cost_usd": round(total_cost, 6)
    }

@app.post("/api/evaluate-output")
def evaluate_output(req: EvalRequest):
    # Simulated LLM-as-a-Judge Evaluation Logic
    has_hallucination = "quantum" in req.response.lower() or "alien" in req.response.lower()
    
    if has_hallucination:
        faithfulness = 0.25
        relevance = 0.60
        hallucination_risk = 0.88
        verdict = "FAILED (Hallucination Detected)"
    else:
        faithfulness = 0.96
        relevance = 0.94
        hallucination_risk = 0.04
        verdict = "PASSED (Grounded)"

    return {
        "query": req.query,
        "faithfulness_score": faithfulness,
        "answer_relevance_score": relevance,
        "hallucination_risk": hallucination_risk,
        "verdict": verdict
    }

@app.get("/api/sample-trace")
def get_sample_trace():
    return {
        "trace_id": "tr-9948a",
        "name": "E-Commerce Support Agent Trace",
        "total_duration_ms": 580.4,
        "spans": [
            {
                "span_id": "sp-01",
                "name": "User Input Preprocessing",
                "type": "CHAIN",
                "duration_ms": 15.2,
                "attributes": {"user.id": "usr_901", "session.id": "sess_881"}
            },
            {
                "span_id": "sp-02",
                "name": "Chroma Vector DB Search",
                "type": "RETRIEVER",
                "duration_ms": 115.0,
                "attributes": {"db.name": "Chroma", "top_k": 3, "retrieved_chunks": 3}
            },
            {
                "span_id": "sp-03",
                "name": "LLM Generation (gpt-4o)",
                "type": "LLM",
                "duration_ms": 450.2,
                "attributes": {"model": "gpt-4o", "prompt_tokens": 1250, "completion_tokens": 140, "ttft_ms": 135}
            }
        ]
    }

@app.get("/api/observability-tools-matrix")
def get_tools_matrix():
    return [
        {
            "name": "LangSmith",
            "type": "SaaS / Proprietary",
            "key_features": "LangChain Tracing, Run Tree, Datasets & Evals, Prompt Playground",
            "best_for": "Tim yang membangun di atas LangChain & LangGraph"
        },
        {
            "name": "Langfuse",
            "type": "Open-Source & SaaS",
            "key_features": "Trace Analytics, Prompt Management SDK, Score Tracking, Self-Hosted",
            "best_for": "Tim yang butuh platform open-source ter-manage & prompt versioning"
        },
        {
            "name": "Helicone",
            "type": "Proxy Gateway",
            "key_features": "Smart Caching, Zero SDK Refactor, Rate Limiting, Header Metadata",
            "best_for": "Integrasi cepat tanpa mengubah codebase (cukup ubah Base URL)"
        },
        {
            "name": "Arize AI / Phoenix",
            "type": "Open-Source & Enterprise",
            "key_features": "Embedding Visualization (UMAP), OpenTelemetry Spans, RAG Evals",
            "best_for": "ML Engineers & Data Scientists yang butuh visualisasi data & drift"
        }
    ]

# Serve Static Web Files
current_dir = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=current_dir), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(current_dir, "index.html"))

if __name__ == "__main__":
    print("🚀 Starting Web Visualizer Server on http://localhost:8000 ...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
