# WEB SOCKET

## library
    cargo add axum --features "json macros ws"
    cargo add tokio --features full
    cargo add serde --features derive
    cargo add chrono
    cargo add serde_json
    cargo add futures
    cargo add futures-util

## note
    <!-- clients: Arc<Mutex<HashMap<String, Arc<WebSocket>>>> -->
    struct AppState {
        clients: Arc<Mutex<HashMap<String, Arc<WebSocket>>>>
    }
    Kamu kemungkinan menyimpan WebSocket seperti ini:
    Arc<Mutex<HashMap<String, Arc<WebSocket>>>>
    Kemudian kamu meng-clone atau spawn ke dalam thread lain (tokio task), sehingga Rust mencoba memastikan semua tipe-nya aman dibagikan ke thread lain.

    Tapi WebSocket dari Axum (yang sebenarnya dari axum::extract::ws::WebSocket) mengandung komponen internal (hyper::upgrade::Io) yang tidak Sync, dan karena itu:

    Tidak bisa di-wrap dalam Arc

    Tidak bisa dimasukkan ke Mutex<HashMap<...>>

    Tidak bisa digunakan di dalam tokio::spawn(...)

    💡 Solusi:
    ✅ Solusi 1: Jangan simpan WebSocket secara langsung
    Alih-alih menyimpan WebSocket di dalam HashMap, kamu bisa:

    Pisahkan WebSocket menjadi sender dan receiver (socket.split() seperti di contohmu)

    Kirim pesan ke masing-masing klien melalui broadcast::Sender

    Tidak perlu menyimpan seluruh objek WebSocket

    Ini adalah pendekatan yang kamu sudah gunakan, dan itu bagus! 😄

    ✅ Solusi 2: Jika kamu perlu simpan dan kirim langsung ke WebSocket
    Kamu harus membuat actor/task untuk masing-masing klien dan hanya kirim pesan melalui tokio::mpsc::Sender, bukan menyimpan WebSocket:

    Contoh:
    let (tx, mut rx) = tokio::sync::mpsc::unbounded_channel::<String>();
    // simpan tx ke HashMap, dan gunakan rx dalam task yang handle socket
    🧠 Catatan Singkat:
    WebSocket bukan Send atau Sync → jangan simpan langsung dalam struktur global.

    Pakai channel (broadcast, mpsc, dsb.) untuk komunikasi antar task.