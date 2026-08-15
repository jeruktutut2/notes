# 📘 Modul 11 — Deployment, Caching & Monitoring

Modul ini mendemonstrasikan bagaimana membungkus aplikasi AI dalam **FastAPI Server** siap produksi yang dilengkapi dengan **Caching Engine** (menghemat latensi & biaya token) serta **Observability Monitoring** (telemetri penggunaan token & biaya).

---

## ⚙️ Komponen Sistem Deployment

1. **`app.py`**: Web API Server berbasis **FastAPI** yang menyediakan endpoint `/v1/chat`, `/health`, `/v1/metrics`, dan `/v1/cache-stats`.
2. **`caching.py`**: Engine Exact Match Caching menggunakan Hashing MD5 untuk mengembalikan respon instan (< 0.01 detik) pada pertanyaan yang sama.
3. **`monitoring.py`**: Pengukur telemetri real-time yang mencatat latensi per request, estimasi jumlah token, dan akumulasi biaya USD.
4. **`Dockerfile` & `docker-compose.yml`**: Konfigurasi kontainerisasi untuk menjalankan FastAPI Backend bersama Service Ollama.

---

## 🚀 Cara Menjalankan (Oleh Pengguna)

### Cara 1: Menjalankan Secara Lokal (Uvicorn)
```bash
# 1. Pastikan Ollama sudah berjalan
ollama serve

# 2. Jalankan Uvicorn ASGI Server dari folder utama
uvicorn 11_deployment.app:app --reload --port 8000

# 3. Akses Swagger UI di browser:
# http://localhost:8000/docs
```

### Cara 2: Menjalankan dengan Docker Compose
```bash
cd 11_deployment
docker-compose up -d
```
