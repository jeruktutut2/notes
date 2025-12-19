# PYTHON3 SPEECH TO TEXT

## library
    python3 -m venv .venv
    python3 -m venv .venv2
    source .venv/bin/activate
    source .venv2/bin/activate
    pip install gunicorn
    pip install "uvicorn[standard]"
    pip install fastapi
    pip install aiortc
    pip install python-multipart
    pip install webrtcvad
    pip install --upgrade setuptools karena muncul error ModuleNotFoundError: No module named 'pkg_resources'
    pip install numpy
    pip install librosa
    pip install "setuptools<81"
    pip install git+https://github.com/openai/whisper.git 
    pip install openai-whisper
    pip install av==10.0.0
    pip install faster-whisper
    pip install --upgrade pip setuptools wheel --
    pip install "faster-whisper[torch]" --
    deactivate
    pip install --upgrade pip

## run
    gunicorn main:app -k uvicorn.workers.UvicornWorker --workers 5 --bind 0.0.0.0:8080
    workers = (2 x CPU cores) + 1, Jika server kamu punya 2 core CPU, maka: workers = (2 x 2) + 1 = 5

## note
    gunakan python3.10 atau 3.9 agar faster-whisper bisa diinstall

set gunicorn timeout