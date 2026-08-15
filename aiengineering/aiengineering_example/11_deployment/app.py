"""
==============================================================================
FASTAPI REST API SERVER UNTUK PRODUKSI APLIKASI AI
==============================================================================
Server REST API tingkat produksi berbasis FastAPI yang membungkus pemanggilan LLM,
dilengkapi dengan Caching Engine, Observability Monitoring, & Endpoint Health Check.

ENDPOINT YANG TERSEDIA:
    - GET  /              : Welcome & API Info
    - GET  /health        : Health check status server & status koneksi LLM
    - POST /v1/chat       : Endpoint utama chat dengan Caching & Monitoring
    - GET  /v1/metrics    : Telemetri penggunaan token, biaya, & latensi
    - GET  /v1/cache-stats: Statistik performa Hit Rate Caching

CARA PAKAI:
    - Jalankan dengan uvicorn: uvicorn app:app --reload --port 8000
    - Buka dokumentasi Swagger UI: http://localhost:8000/docs
==============================================================================
"""

import os
import time
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from caching import ExactMatchCache
from monitoring import monitor_global

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL = os.getenv("DEFAULT_MODEL", "gemma3:4b")

# Inisialisasi Aplikasi FastAPI & Cache Engine
app = FastAPI(
    title="AI Engineering Production REST API",
    description="Backend API Siap Produksi dengan Caching & Observability",
    version="1.0.0"
)

cache_engine = ExactMatchCache(ttl_seconds=3600)  # TTL 1 Jam


# ------------------------------------------------------------------------------
# REQUEST & RESPONSE SCHEMAS (PYDANTIC)
# ------------------------------------------------------------------------------

class ChatRequest(BaseModel):
    prompt: str = Field(description="Pertanyaan pengguna", example="Apa fungsi utama FastAPI?")
    system_prompt: str = Field(default="Kamu adalah asisten AI yang membantu.", description="System prompt opsional")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Kreativitas AI")


class ChatResponse(BaseModel):
    response: str
    cached: bool
    latency_sec: float
    model_used: str


# ------------------------------------------------------------------------------
# ENDPOINTS LAYANAN API
# ------------------------------------------------------------------------------

@app.get("/")
def read_root():
    return {
        "message": "Selamat datang di Production AI API Server!",
        "docs_url": "http://localhost:8000/docs"
    }


@app.get("/health")
def health_check():
    """Mengecek kesehatan server dan konektivitas ke Ollama."""
    try:
        res = requests.get("http://localhost:11434/api/tags", timeout=3)
        ollama_status = "ONLINE" if res.status_code == 200 else "UNHEALTHY"
    except Exception:
        ollama_status = "OFFLINE"

    return {
        "status": "OK",
        "ollama_backend": ollama_status,
        "model_default": MODEL
    }


@app.post("/v1/chat", response_model=ChatResponse)
def handle_chat(req: ChatRequest):
    """Endpoint utama pemrosesan pesan pengguna dengan fitur Caching."""
    start_time = time.time()

    # 1. Cek Caching terlebih dahulu (Exact Match)
    cached_res = cache_engine.get(req.prompt, req.system_prompt)
    if cached_res:
        durasi = time.time() - start_time
        # Catat tetap di monitoring
        monitor_global.catat_request(req.prompt, cached_res, durasi)
        return ChatResponse(
            response=cached_res,
            cached=True,
            latency_sec=round(durasi, 4),
            model_used=MODEL
        )

    # 2. Jika Cache Miss -> Panggil Ollama API
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": req.system_prompt},
            {"role": "user", "content": req.prompt}
        ],
        "stream": False,
        "options": {"temperature": req.temperature}
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=30)
        res.raise_for_status()
        raw_res = res.json()["message"]["content"]

        durasi = time.time() - start_time

        # 3. Simpan ke Cache & Catat Telemetri Monitoring
        cache_engine.set(req.prompt, raw_res, req.system_prompt)
        monitor_global.catat_request(req.prompt, raw_res, durasi)

        return ChatResponse(
            response=raw_res,
            cached=False,
            latency_sec=round(durasi, 4),
            model_used=MODEL
        )

    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Ollama backend service is offline.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Engine Error: {str(e)}")


@app.get("/v1/metrics")
def get_telemetry_metrics():
    """Mengembalikan data statistik penggunaan token, biaya, dan rata-rata latensi."""
    return monitor_global.get_summary_metrics()


@app.get("/v1/cache-stats")
def get_cache_statistics():
    """Mengembalikan data Hit Rate perbandingan pemanggilan cache vs miss."""
    return cache_engine.get_stats()
