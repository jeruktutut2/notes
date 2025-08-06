# PYTHON3 VAD

## library
    python3 -m venv .venv
    source .venv/bin/activate
    pip install fastapi
    pip install 'uvicorn[standard]'
    pip install aiortc
    pip install python-multipart
    pip install webrtcvad
    pip install --upgrade setuptools karena muncul error ModuleNotFoundError: No module named 'pkg_resources'
    pip install numpy
    deactivate
    uvicorn main:app --reload --port 8080
    pip install --upgrade pip