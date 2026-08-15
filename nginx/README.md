# NGINX

## Install
    sudo apt update
    sudo apt install nginx

## Buat config site
    sudo nano /etc/nginx/sites-available/default
    sudo nano /etc/nginx/sites-available/teleponapp

```
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;

        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # penting untuk FastAPI / streaming / websocket
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

```
server {
    listen 80;
    server_name _;

    # ---- SSE (harus lebih spesifik) ----
    location /sse/ {
        proxy_pass http://127.0.0.1:8000;

        gzip off;
        proxy_buffering off;
        proxy_cache off;
        # proxy_read_timeout 1h;
        proxy_read_timeout 1d;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # ------------------------
    # API → Python
    # ------------------------
    location /api/ {
        proxy_pass http://127.0.0.1:8000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # ------------------------
    # WebSocket → Python
    # ------------------------
    location /ws/ {
        proxy_pass http://127.0.0.1:8000;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # ------------------------
    # selain /api dan /ws
    # → frontend :3000
    # ------------------------
    location / {
        proxy_pass http://127.0.0.1:3000;

        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Enable site
    sudo ln -s /etc/nginx/sites-available/teleponapp /etc/nginx/sites-enabled

## Test config
    sudo nginx -t

## Reload nginx
    sudo systemctl reload nginx

## Restart nginx
    sudo systemctl restart nginx

## Remove config
    Cek dulu: myapp itu aktif dari mana
    ls -l /etc/nginx/sites-enabled/
    Biasanya akan terlihat:
    myapp -> /etc/nginx/sites-available/myapp
    Artinya:
    👉 yang aktif itu symlink.

    Nonaktifkan (ini yang benar & aman)
    Jangan langsung hapus file aslinya.
    Cukup hapus symlink-nya saja:
    sudo rm /etc/nginx/sites-enabled/teleponapp

    👉 Setelah ini:
    config myapp sudah tidak dipakai nginx

    Test config
    sudo nginx -t

    Pastikan:
    syntax is ok
    test is successful

    Reload nginx
    sudo systemctl reload nginx
    🧠 Sampai di sini, myapp sudah benar-benar tidak aktif.
    🗑️ (Opsional) Kalau mau hapus filenya sekalian
    Kalau kamu yakin sudah tidak dipakai lagi:
    sudo rm /etc/nginx/sites-available/myapp

## Edit default
    Buka file default
    sudo nano /etc/nginx/sites-available/default
    sudo nginx -t
    sudo systemctl reload nginx
    grep -R "server_name _" /etc/nginx/sites-enabled