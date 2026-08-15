# Distributed Session

Proyek ini mendemonstrasikan cara membuat sistem manajemen sesi terdistribusi (Distributed Session) menggunakan **Redis** sebagai penyimpanan *state* secara terpusat (Centralized State).

## 🧩 Mengapa Session Harus Terdistribusi?
Jika kita memiliki 5 instance/server API (misal Node A, B, C, D, E) di balik *Load Balancer*, dan kita menyimpan *login session* di dalam memori internal (RAM) Node A:
- Saat user login dan dilayani oleh Node A, dia berhasil masuk.
- Permintaan (*request*) berikutnya dari user tersebut diarahkan oleh Load Balancer ke Node C.
- Karena Node C tidak tahu soal memori Node A, Node C akan menganggap user tersebut belum login (401 Unauthorized).

## 💡 Solusi: Centralized Redis Session
Semua 5 instance aplikasi tidak menyimpan status login (Stateless API). Ketika ada *request* masuk yang membawa `session_id`, siapapun Node yang menerima request tersebut akan melakukan *lookup* ke server Redis terpusat.

Konsep lain yang ditunjukkan di sini adalah **Sliding Expiration**. Saat user aktif menggunakan aplikasi, TTL (Time-To-Live) dari session tersebut terus diperpanjang (di-refresh) di Redis agar user tidak tiba-tiba ter-logout.

## 🚀 Cara Menjalankan
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```
Script akan mencontohkan proses Login (mendapatkan Session ID dari Redis), mengakses profil menggunakan ID tersebut, dan melakukan Logout (menghapus key di Redis).
