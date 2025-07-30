# GOLANG WEBRTC

## library
    go get github.com/labstack/echo/v4
    go get github.com/pion/webrtc
    go get github.com/pion/webrtc/v3@latest
    go get github.com/pion/webrtc/v4
    go get github.com/gorilla/websocket
    go get github.com/google/uuid
    go get github.com/hraban/opus

    Jika kamu menggunakan Ubuntu/Debian:
    sudo apt update
    sudo apt install libopus-dev

    Jika kamu menggunakan Alpine (Docker):
    apk add opus-dev pkgconfig

    Jika kamu menggunakan macOS (dengan Homebrew):
    brew install opus

    🔍 Kenapa ini perlu?
    Library github.com/hraban/opus adalah Go wrapper untuk library C libopus. Saat kompilasi, Go akan menggunakan pkg-config untuk mencari file opus.pc dari libopus. Jika tidak ditemukan, muncul error seperti:
    Package opus was not found in the pkg-config search path.

    🛠 1. Install libopusfile
    Untuk Ubuntu/Debian:
    sudo apt install libopusfile-dev
    
    Untuk macOS (Homebrew):
    brew install opusfile
    
    Untuk Alpine Linux:
    apk add opusfile-dev

    menambahkan ffmpeg
    brew install ffmpeg
    ffmpeg -version