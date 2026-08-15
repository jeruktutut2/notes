# BUCKET REDIS

## note
Berikut contoh rate-limiting token bucket berbasis Redis untuk Golang Echo v5
(aman untuk multi-instance / multi-pod).
Kita pakai:
- Redis
- Lua script (biar atomic)
- per-IP
- model: token bucket

```bash
go get github.com/redis/go-redis/v9
```

🧠 Konsep singkat
Di Redis kita simpan:
tokens → jumlah token saat ini
ts → last refill timestamp (ms)
Setiap request:
hitung token baru berdasarkan waktu
kurangi 1 token
kalau token < 1 → reject
Semua dilakukan di Lua (atomic).

🔎 Artinya konfigurasi ini
capacity = 20
refillPerSecond = 10

Sama persis dengan:
rate.NewLimiter(10, 20)

yang sebelumnya (in-memory).

⚠️ Penting (konteks yang nyambung dengan diskusi kamu sebelumnya)
1️⃣ Ini cocok untuk multi instance
Karena state ada di Redis.
Kalau kamu deploy:
3 pod Echo
1 Redis
→ rate limit tetap konsisten.

2️⃣ Redis jadi bagian dari critical path
Per request ada:
1 EVAL (Lua)
Jadi:
pastikan Redis dekat (latency kecil)
beri timeout (di contoh sudah ada 200ms)

3️⃣ Soal context & client disconnect
Perhatikan ini:

ctx, cancel := context.WithTimeout(
    c.Request().Context(),
    200*time.Millisecond,
)

Artinya:

👉 kalau client disconnect / request dibatalkan,
atau Redis lambat,
Lua call akan ikut cancel.
Ini nyambung dengan topik yang sering kamu bahas:
cancellation propagation.

🧪 Test dengan curl
Sama persis seperti versi non-Redis:

for i in {1..50}; do
  curl -s -o /dev/null -w "%{http_code}\n" http://localhost:1323/
done

atau versi 100ms:

for i in {1..100}; do
  curl -s -o /dev/null -w "%{http_code}\n" http://localhost:1323/
  sleep 0.1
done

for i in {1..100}; do
  curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/
  sleep 0.1
done

🧠 Catatan kecil (penting)
Implementasi ini benar-benar:

👉 token bucket
bukan sliding window, bukan fixed window.
Jadi perilakunya akan sangat mirip dengan:
golang.org/x/time/rate.
Pertanyaan ini bagus — dan ini memang poin paling penting kalau rate limit pakai Redis.

Jawaban pendeknya:

👉 karena kita butuh operasi yang atomic di Redis.
Sekarang saya jelaskan pelan dan sangat konkret.

🎯 Masalah utama tanpa Lua
Algoritma token bucket itu butuh beberapa langkah:
baca tokens
baca last timestamp
hitung refill
update tokens
update timestamp
tentukan boleh / tidak
Kalau kamu lakukan di Go:

HGET tokens
HGET ts
→ hitung di Go
HSET tokens
HSET ts

👉 ini bukan atomic.

🔥 Contoh race condition

Misalnya:
tokens = 1
Lalu ada 2 request masuk hampir bersamaan.
Request A
HGET tokens → 1
Request B
HGET tokens → 1
Dua-duanya mikir:
masih ada token
Lalu:

A → HSET tokens = 0
B → HSET tokens = 0

👉 hasilnya:
2 request lolos,
padahal seharusnya hanya 1.

🧠 Ini sangat relevan dengan background kamu
Kamu sering bahas:
concurrency
database
transaction
race condition
Ini kasus yang sama.

✅ Kenapa Lua menyelesaikan masalah ini?
Karena di Redis:
satu script Lua dieksekusi secara atomik
Artinya:
selama script jalan
tidak ada command lain yang bisa nyelip
Jadi:

baca → hitung → update → return

terjadi sebagai satu kesatuan.

⚠️ Kenapa tidak pakai MULTI / EXEC saja?
Banyak yang mikir:
pakai Redis transaction (MULTI / EXEC)

Masalahnya:
MULTI / EXEC itu:
hanya menjamin command dieksekusi berurutan
tapi logika hitungnya di client

Contoh:

WATCH key
HGET
HGET
MULTI
HSET
HSET
EXEC

👉 bisa, tapi:
jauh lebih rumit
retry logic harus kamu tangani sendiri
lebih banyak round-trip

🔎 Kenapa tidak cukup pakai INCR / EXPIRE?
Karena:
token bucket butuh:
refill berbasis waktu
fractional token
bukan cuma hitung request
INCR cocoknya:

👉 fixed window / sliding window sederhana
Bukan token bucket.

🧩 Jadi alasan teknisnya ada 3
1️⃣ Atomicity
Ini yang utama.

2️⃣ Konsistensi antar instance
Kalau kamu punya:
3 server
100 request paralel
Lua menjamin:
per key, keputusan allow / deny konsisten.

3️⃣ Lebih dekat ke data
Perhitungan:

token = min(capacity, token + delta * rate)

langsung dilakukan di Redis.
Lebih sedikit bolak-balik network.

🧠 Ringkas tapi tepat
Kalau kamu mau satu kalimat yang tepat:
Kita pakai Lua karena token bucket membutuhkan read–modify–write yang harus atomic, dan Redis hanya bisa menjamin itu dengan Lua script.
🧨 Kalau kamu tidak pakai Lua, apa risikonya?

Jawaban jujurnya:

👉 rate limit kamu akan bocor di kondisi concurrency tinggi.
Dan bocornya bukan:
error
panic
Tapi:
lebih banyak request lolos dari limit.
Ini yang paling berbahaya.

Kalau mau, setelah ini saya bisa tunjukkan versi:
➡️ rate limit Redis tanpa Lua
➡️ lalu kita bandingkan race condition-nya (secara konsep) supaya makin kebayang.