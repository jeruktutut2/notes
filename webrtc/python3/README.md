# PYTHON3 WEBRTC

## library
    python3 -m venv .venv
    pip install --upgrade pip
    source .venv/bin/activate
    pip install 'fastapi uvicorn[standard] aiortc python-multipart'
    pip install fastapi
    pip install 'uvicorn[standard]'
    pip install aiortc
    pip install python-multipart
    deactivate
    uvicorn main:app --reload --port 8080