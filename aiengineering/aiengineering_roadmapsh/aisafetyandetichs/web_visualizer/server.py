"""
FastAPI Server to serve the AI Safety and Ethics Web Visualizer & API Endpoints
"""

import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI(title="AI Safety & Ethics Visualizer API")

# Path to static web visualizer dir
STATIC_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "AI Safety & Ethics Learning Visualizer"}

# Serve index.html at root
@app.get("/")
def read_root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

# Mount static files (CSS, JS)
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

if __name__ == "__main__":
    print("Starting AI Safety and Ethics Web Visualizer at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
