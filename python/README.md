# PYTHON

## note
    cek installed python
    which python3
    type -a python3
    biasanya hasilnya
    python3 is /usr/local/bin/python3
    python3 is /usr/bin/python3

    jika ls -l /usr/local/bin/python3 dan hasilnya kira-kira lrwxr-xr-x  1 user  admin  37 Jul 27 14:13 /usr/local/bin/python3 -> ../Cellar/python@3.10/3.10.13/bin/python3 berarti itu symlink ke Homebrew.

    brew list python
    brew install python@3.10 install python3.10, untuk kebutuhan open-whisper
    buat symlink
    ln -sf /usr/local/opt/python@3.10/bin/python3 /usr/local/bin/python3
    ln -sf /usr/local/opt/python@3.10/bin/pip3 /usr/local/bin/pip3
    brew --prefix python@3.10 melihat path-nya yang benar

    brew install pyenv seperti sdkman pada java
    🔹 Contoh penggunaan pyenv
    Install pyenv (kalau pakai Homebrew di Mac):
    brew install pyenv
    Install versi Python tertentu:
    pyenv install 2.7.18
    pyenv install 3.11.5
    pyenv install 3.12.2

    Cek versi yang sudah terinstall:
    pyenv versions
    Set versi global (seluruh sistem):
    pyenv global 3.11.5
    Set versi lokal (khusus project folder):
    cd proyek-lama
    pyenv local 2.7.18   # hanya berlaku di folder ini
    Set versi hanya untuk 1 kali eksekusi:
    pyenv shell 3.12.2

## install
    apa beda virtual environment dengan pyenv?
    ChatGPT said:
    Mantap pertanyaan ini 👌, karena banyak orang awalnya bingung bedain virtual environment (venv, virtualenv, conda env) dengan pyenv.
    Padahal keduanya beda level fungsinya.

    🔹 1. pyenv
    👉 Manajer versi Python (interpreter).
    Fungsinya: install, ganti, dan kelola versi Python di 1 komputer.
    Contoh: punya Python 2.7.18, 3.9.13, dan 3.11.6 di 1 laptop.
    Kamu bisa pilih versi mana yang jadi global default atau hanya untuk folder project tertentu.
    Tidak peduli package apa yang dipakai, fokusnya ke interpreter Python.
    Contoh pakai pyenv:
    pyenv install 3.11.6
    pyenv install 2.7.18
    pyenv local 2.7.18   # di folder project ini, pakai Python 2
    pyenv global 3.11.6  # di sistem global, default pakai Python 3.11

    🔹 2. Virtual environment (venv / virtualenv / conda env)
    👉 Manajer library/dependencies (paket yang diinstall via pip atau conda).
    Fungsinya: bikin lingkungan terisolasi supaya tiap project punya package sendiri.
    Kalau tidak pakai venv, semua pip install akan masuk ke global site-packages → rawan bentrok antar project.
    Cocok buat menghindari konflik dependency.
    Contoh pakai venv:
    python3 -m venv venv
    source venv/bin/activate   # aktifkan
    pip install flask==2.2.0   # cuma ada di env ini

    🔹 Bedanya
    Fitur	pyenv	virtualenv / venv
    Level	Interpreter Python	Dependencies (package)
    Tujuan	Ganti versi Python (2.7, 3.8, 3.11, dst)	Pisahkan library antar project
    Contoh masalah yang diselesaikan	Project lama butuh Python 2.7, project baru butuh Python 3.11	Project A butuh Django 2.2, Project B butuh Django 4.0
    Bisa dipakai bareng?	✅ Iya	✅ Iya
    🔹 Kombinasi Ideal
    Biasanya dipakai bersama:
    Pakai pyenv untuk pilih versi Python sesuai project.
    Di dalamnya, bikin virtual environment untuk kelola dependency.

    Contoh workflow:
    # pilih Python versi 3.11 untuk project ini
    pyenv local 3.11.6  

    # bikin virtual environment dengan Python 3.11
    python -m venv venv  

    # aktifkan
    source venv/bin/activate  

    # install package khusus project ini
    pip install fastapi uvicorn

    👉 Jadi singkatnya:
    pyenv = atur mesinnya (Python mana yang dipakai).
    venv/virtualenv = atur isinya (library apa yang dipakai project).

    pyenv install 2.7.18
    cd /path/to/projek
    pyenv local 2.7.18
    python -m virtualenv venv
    source venv/bin/activate

    set path
    Shims pyenv tidak ada di PATH
    Coba cek:
    echo $PATH | grep pyenv

    Kalau tidak ada ~/.pyenv/shims, maka python dari pyenv tidak akan bisa ditemukan.
    ✅ Solusi: pastikan di ~/.bashrc, ~/.zshrc, atau ~/.profile ada baris:

    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"   # kalau pakai pyenv-virtualenv

    Python 2.7.18 belum diinstall
    Jalankan:
    pyenv versions

    Pastikan ada 2.7.18 di daftar.
    Kalau tidak ada, install dulu:
    pyenv install 2.7.18
    .python-version sudah diset tapi interpreter tidak tersedia
    Misalnya .python-version berisi 2.7.18, tapi versi itu belum pernah diinstall.
    Maka pyenv akan bingung → python tidak ditemukan.

    Conflict dengan Homebrew/system python
    Kadang Homebrew path lebih duluan daripada pyenv shims.
    Coba cek interpreter aktif:

    which python
    which python3

    Kalau hasilnya /usr/local/bin/python atau /opt/homebrew/bin/python → berarti pyenv belum override.

    3. Kalau kamu ragu/racamp shell
    Cek dulu dengan:
    echo $SHELL
    Kalau hasilnya /bin/zsh → edit ~/.zshrc
    Kalau hasilnya /bin/bash → edit ~/.bash_profile

    ✅ Solusi untuk Python 2.7
    Kalau mau bikin virtual environment di Python 2, kamu harus pakai virtualenv (bukan venv).
    Install dulu virtualenv di Python 2.7 (via pyenv):
    pyenv exec pip install virtualenv
    (pastikan sudah pyenv local 2.7.18 di folder project supaya pip mengacu ke Python 2.7)
    Buat virtual environment:
    pyenv exec virtualenv .venv2
    atau kalau mau jelas ke interpreter Python 2.7:
    ~/.pyenv/versions/2.7.18/bin/python -m virtualenv .venv2
    Aktifkan:
    source .venv2/bin/activate

    Oke 👍 di macOS instalasi pyenv cukup mudah, biasanya lewat Homebrew. Berikut langkah-langkahnya:
    🔹 1. Pastikan Homebrew sudah ada
    Cek:
    brew --version
    Kalau belum ada, install dulu:
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    🔹 2. Install pyenv
    brew install pyenv
    curl https://pyenv.run | bash

    🔹 3. (Opsional tapi disarankan) Install pyenv-virtualenv
    Supaya mudah bikin virtual environment:
    brew install pyenv-virtualenv

    🔹 4. Tambahkan ke shell
    Anda harus menambahkan inisialisasi pyenv ke shell config (~/.zshrc kalau pakai Zsh, ~/.bashrc kalau pakai Bash). Tambahkan baris berikut:

    Cek dulu dengan:
    echo $SHELL
    Kalau hasilnya /bin/zsh → edit ~/.zshrc
    Kalau hasilnya /bin/bash → edit ~/.bash_profile

    # pyenv init
    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"

    Lalu reload shell:
    exec "$SHELL"

    🔹 5. Cek instalasi
    pyenv --version
    pyenv versions
    which python
    pyenv which python

    🔹 6. Install Python versi tertentu
    Contoh:
    pyenv install 3.12.4
    pyenv install 3.11.9
    pyenv install 3.9.18
    Lihat daftar Python yang tersedia:
    pyenv install --list

    🔹 7. Pilih versi
    Global (semua project default)
    pyenv global 3.12.4
    Per project (folder tertentu)
    pyenv local 3.11.9
    pyenv local 3.9.18
    
    → ini akan membuat file .python-version di folder project.

    ⚡ Setelah ini, setiap kali Anda masuk ke folder project, pyenv akan otomatis mengatur versi Python sesuai .python-version.

    × Getting requirements to build wheel did not run successfully. │ exit code: 1 ╰─> [17 lines of output] Package libavformat was not found in the pkg-config search path. Perhaps you should add the directory containing libavformat.pc' to the PKG_CONFIG_PATH environment variable Package 'libavformat' not found Package 'libavcodec' not found Package 'libavdevice' not found Package 'libavutil' not found Package 'libavfilter' not found Package 'libswscale' not found Package 'libswresample' not found Warning! You are using an EOL, unsupported, and out-of-date OS. Warning! You are installing from source. It is EXPECTED that it will fail. You are REQUIRED to use ffmpeg 7. You MUST have Cython, pkg-config, and a C compiler. pkg-config could not find libraries ['avformat', 'avcodec', 'avdevice', 'avutil', 'avfilter', 'swscale', 'swresample'] [end of output] pada saat pip install aiortc

    ➡️ Python sedang mencoba meng-compile modul aiortc, yang butuh FFmpeg libraries (libavformat, libavcodec, libavutil, dll).
    Tapi library itu tidak ditemukan di sistem kamu — jadi pkg-config tidak bisa memberitahu compiler di mana letaknya.

    pkg-config could not find libraries ['avformat', 'avcodec', 'avdevice', 'avutil', 'avfilter', 'swscale', 'swresample']
    ➡️ Semua komponen utama FFmpeg belum terinstal atau tidak dikenali.

    Warning! You are installing from source.
    It is EXPECTED that it will fail. You are REQUIRED to use ffmpeg 7.
    You MUST have Cython, pkg-config, and a C compiler.
    ➡️ Karena tidak ada wheel prebuilt (paket biner siap pakai) untuk platform kamu, pip mencoba membangun dari source.
    Tapi itu akan gagal kalau kamu tidak punya:
    FFmpeg 7 (dan dev headers)
    pkg-config
    gcc (C compiler)
    Cython

    🧩 Solusi (untuk Linux/Ubuntu/Debian)
    Jalankan ini dulu sebelum pip install aiortc:
    sudo apt update
    sudo apt install -y ffmpeg libavformat-dev libavcodec-dev libavdevice-dev \
        libavutil-dev libavfilter-dev libswscale-dev libswresample-dev \
        pkg-config python3-dev build-essential cython3
    Lalu ulangi:
    pip install aiortc

    🧩 Solusi (untuk macOS)
    Gunakan Homebrew:
    brew install ffmpeg pkg-config cython
    Kemudian:
    pip install aiortc