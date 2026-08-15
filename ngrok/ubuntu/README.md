# NGROK UBUNTU

## Install
    ✅ 1. Download & install ngrok di Ubuntu
    Masuk ke server kamu, lalu:
    ```bash
    cd /tmp
    curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
    sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null

    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
    sudo tee /etc/apt/sources.list.d/ngrok.list

    sudo apt update
    sudo apt install ngrok
    ```
    Atau:
    ```bash
    curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
    | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
    && echo "deb https://ngrok-agent.s3.amazonaws.com bookworm main" \
    | sudo tee /etc/apt/sources.list.d/ngrok.list \
    && sudo apt update \
    && sudo apt install ngrok
    ```
    Cek:
    ```bash
    ngrok version
    ```
    Kalau muncul versi → install sudah OK.

    ✅ 2. Login / set authtoken
    Buka website ngrok, login, lalu copy authtoken.
    Di server:  
    ```bash
    ngrok config add-authtoken TOKEN_KAMU
    ```
    Contoh:
    ```bash
    ngrok config add-authtoken 2Xxxxxxxxxxxxxxxxxxxxxxxxx
    ```
    Setelah ini, file config otomatis dibuat di:
    ```bash
    ~/.config/ngrok/ngrok.yml
    cat /root/.config/ngrok/ngrok.yml
    ```

    ✅ 3. Jalankan ngrok ke nginx (ini yang kamu butuhkan)
    Karena nginx kamu listen di port 80:

    ```bash
    ngrok http 80
    ```
    Selesai.    
    Biasanya akan muncul seperti:
    ```bash
    Forwarding  https://abcd-xxx.ngrok-free.app -> http://localhost:80
    ```

## systemd
    Cara paling disarankan: pakai systemd
    Dengan ini, ngrok:
    - jalan di background
    - bisa auto-start saat boot
    - bisa dilihat log-nya

    Konsisten dengan cara kamu menjalankan teleponapp.service sebelumnya

    1️⃣ Pastikan ngrok sudah bisa jalan manual
    Cek dulu:
    ```bash
    ngrok http 80
    ```
    Kalau sudah keluar URL → lanjut.

    2️⃣ Cari lokasi binary ngrok
    ```bash
    which ngrok
    ```

    Biasanya hasilnya:
    /usr/bin/ngrok
    /root/.pyenv/shims/ngrok
    Catat path-nya.

    3️⃣ Buat service file
    ```bash
    sudo nano /etc/systemd/system/teleponngrok.service
    ```

    Isi seperti ini:

    ```bash
    [Unit]
    Description=ngrok tunnel for nginx
    After=network.target

    [Service]
    Type=simple
    Environment=HOME=/root
    ExecStart=/root/.pyenv/shims/ngrok http 80
    Restart=always
    RestartSec=5

    [Install]
    WantedBy=multi-user.target
    ```

    ⚠️ Pastikan /usr/bin/ngrok sesuai dengan hasil which ngrok.
    4️⃣ Reload systemd
    ```bash
    sudo systemctl daemon-reload
    ```
    5️⃣ Jalankan ngrok di background
    ```bash
    sudo systemctl start teleponngrok
    ```
    6️⃣ Cek status
    ```bash
    sudo systemctl status teleponngrok
    ```

    Kalau normal, statusnya:
    ```bash
    Active: active (running)
    ```

    7️⃣ Supaya otomatis jalan saat boot
    ```bash
    sudo systemctl enable teleponngrok
    ```
    ✅ Melihat URL ngrok (karena jalan di background)
    Karena sekarang ngrok tidak tampil di terminal, kamu bisa lihat URL-nya dari log:
    ```bash
    journalctl -u teleponngrok -n 50 --no-pager
    ```

    Biasanya ada baris seperti:
    ```bash
    Forwarding https://xxxx.ngrok-free.app -> http://localhost:80
    ```