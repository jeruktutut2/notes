"""
=================================================================
3. FASTAPI MODEL SERVING
=================================================================
Membuat REST API sendiri untuk melayani model ML menggunakan
FastAPI — framework Python yang cepat dan modern.

Mengapa FastAPI?
✅ Performa tinggi (berbasis Starlette + async)
✅ Auto-generate dokumentasi (Swagger UI)
✅ Type hints & validation otomatis (Pydantic)
✅ Support async/await
✅ Mudah integrasi dengan PyTorch/TF

Arsitektur:
Client → FastAPI → Model → Response
   ↑                          ↓
   └──────────────────────────┘
=================================================================
"""

# =====================================================
# JALANKAN SERVER:
#   uvicorn 3_fastapi_model_serving:app --reload --port 8000
#
# AKSES DOCS:
#   http://localhost:8000/docs (Swagger UI)
#   http://localhost:8000/redoc (ReDoc)
#
# TEST ENDPOINT:
#   curl -X POST http://localhost:8000/predict \
#     -H "Content-Type: application/json" \
#     -d '{"text": "I love this product!"}'
# =====================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────
# 1. DEFINISI SCHEMA (Request & Response)
# ─────────────────────────────────────────────────────

class PredictRequest(BaseModel):
    """Schema untuk request prediksi."""
    text: str = Field(..., min_length=1, max_length=5000, 
                      description="Teks yang ingin dianalisis")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "This product is absolutely amazing!"
            }
        }


class PredictResponse(BaseModel):
    """Schema untuk response prediksi."""
    text: str
    label: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    inference_time_ms: float
    model_name: str


class BatchPredictRequest(BaseModel):
    """Schema untuk batch prediction."""
    texts: list[str] = Field(..., min_length=1, max_length=32,
                             description="List teks (maks 32)")


class BatchPredictResponse(BaseModel):
    """Schema untuk batch response."""
    predictions: list[PredictResponse]
    total_inference_time_ms: float
    batch_size: int


class HealthResponse(BaseModel):
    """Schema untuk health check."""
    status: str
    model_loaded: bool
    model_name: str
    uptime_seconds: float


# ─────────────────────────────────────────────────────
# 2. INISIALISASI APP & MODEL
# ─────────────────────────────────────────────────────

app = FastAPI(
    title="🤖 ML Model Serving API",
    description="REST API untuk sentiment analysis menggunakan DistilBERT",
    version="1.0.0",
)

# Global variables untuk model
MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
LABEL_MAP = {0: "NEGATIVE", 1: "POSITIVE"}
tokenizer = None
model = None
start_time = time.time()


@app.on_event("startup")
async def load_model():
    """Muat model saat server startup (hanya 1x)."""
    global tokenizer, model
    logger.info(f"📦 Memuat model: {MODEL_NAME}...")
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.eval()
    
    param_count = sum(p.numel() for p in model.parameters())
    logger.info(f"✅ Model dimuat! ({param_count:,} parameter)")


# ─────────────────────────────────────────────────────
# 3. ENDPOINTS
# ─────────────────────────────────────────────────────

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint — untuk monitoring & load balancer."""
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        model_name=MODEL_NAME,
        uptime_seconds=time.time() - start_time
    )


@app.post("/predict", response_model=PredictResponse, tags=["Inference"])
async def predict(request: PredictRequest):
    """
    Prediksi sentiment untuk satu teks.
    
    - **text**: Teks yang ingin dianalisis (maks 5000 karakter)
    - Returns: label (POSITIVE/NEGATIVE), confidence, dan waktu inference
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model belum dimuat")

    start = time.time()

    # Tokenisasi
    inputs = tokenizer(
        request.text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512
    )

    # Inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Post-processing
    probs = torch.softmax(outputs.logits, dim=-1)
    pred_idx = torch.argmax(probs, dim=-1).item()
    confidence = probs[0][pred_idx].item()

    inference_time = (time.time() - start) * 1000

    return PredictResponse(
        text=request.text,
        label=LABEL_MAP[pred_idx],
        confidence=round(confidence, 4),
        inference_time_ms=round(inference_time, 2),
        model_name=MODEL_NAME
    )


@app.post("/predict/batch", response_model=BatchPredictResponse, tags=["Inference"])
async def predict_batch(request: BatchPredictRequest):
    """
    Prediksi sentiment untuk multiple teks sekaligus (batch).
    
    - **texts**: List teks (maks 32 item)
    - Returns: List prediksi untuk setiap teks
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model belum dimuat")

    if len(request.texts) > 32:
        raise HTTPException(status_code=400, detail="Maks 32 teks per batch")

    start = time.time()

    # Batch tokenisasi
    inputs = tokenizer(
        request.texts,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512
    )

    # Batch inference
    with torch.no_grad():
        outputs = model(**inputs)

    # Post-processing
    probs = torch.softmax(outputs.logits, dim=-1)
    pred_indices = torch.argmax(probs, dim=-1)

    total_time = (time.time() - start) * 1000

    predictions = []
    for i, text in enumerate(request.texts):
        pred_idx = pred_indices[i].item()
        predictions.append(PredictResponse(
            text=text,
            label=LABEL_MAP[pred_idx],
            confidence=round(probs[i][pred_idx].item(), 4),
            inference_time_ms=round(total_time / len(request.texts), 2),
            model_name=MODEL_NAME
        ))

    return BatchPredictResponse(
        predictions=predictions,
        total_inference_time_ms=round(total_time, 2),
        batch_size=len(request.texts)
    )


# ─────────────────────────────────────────────────────
# 4. MAIN (untuk demo tanpa server)
# ─────────────────────────────────────────────────────

def demo_tanpa_server():
    """Jika dijalankan langsung (bukan via uvicorn), tampilkan info."""
    print("=" * 60)
    print("FastAPI Model Serving — Panduan")
    print("=" * 60)

    print("""
    📋 CARA MENJALANKAN:

    1. Jalankan server:
       uvicorn 3_fastapi_model_serving:app --reload --port 8000

    2. Buka dokumentasi API:
       http://localhost:8000/docs

    3. Test dengan curl:
       
       # Health Check
       curl http://localhost:8000/health

       # Single Prediction
       curl -X POST http://localhost:8000/predict \\
         -H "Content-Type: application/json" \\
         -d '{"text": "I love this product!"}'

       # Batch Prediction
       curl -X POST http://localhost:8000/predict/batch \\
         -H "Content-Type: application/json" \\
         -d '{"texts": ["Great movie!", "Terrible service."]}'

    4. Test dengan Python:
       
       import requests
       
       resp = requests.post("http://localhost:8000/predict", json={
           "text": "This is an amazing product!"
       })
       print(resp.json())

    📦 PRODUCTION CHECKLIST:
    ✅ Health check endpoint (/health)
    ✅ Input validation (Pydantic)
    ✅ Batch endpoint (throughput)
    ✅ Error handling (HTTPException)
    ✅ Logging
    ✅ Model loading at startup (bukan per-request)
    ✅ API documentation (auto-generated)
    
    🚀 DEPLOY KE PRODUCTION:
    - Docker: Buat Dockerfile, deploy ke Cloud Run/ECS
    - Kubernetes: Deploy sebagai pod dengan HPA
    - Serverless: AWS Lambda + API Gateway (model kecil)
    """)


if __name__ == "__main__":
    demo_tanpa_server()
