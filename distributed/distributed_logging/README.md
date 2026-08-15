# Distributed Logging (Loki, Promtail, Grafana & Zap JSON Logger)

Proyek ini mendemonstrasikan bagaimana mengumpulkan, menyimpan, dan mencari miliaran baris log dari puluhan server *Microservices* ke dalam satu tempat yang terpusat.

## 🤯 Mengapa Log Harus Terpusat?
Jika Anda punya 10 *container* Docker, dan salah satunya *crash* karena error, bagaimana Anda tahu *container* mana yang error? Anda tidak mungkin melakukan `docker logs` atau `tail -f` satu per satu ke 10 *container* tersebut. 
Log harus disedot dan dikumpulkan di satu "Danau Log" (Log Lake) agar bisa di- *query* dengan mudah.

## 🧱 The Stack (PLG)
Proyek ini menggunakan stack PLG yang ringan (lebih ringan dibanding ELK - Elasticsearch Logstash Kibana):
1. **Promtail**: Agen pencuri log. Berjalan di setiap server, tugasnya membaca file `app.log` lalu mengirim isinya.
2. **Loki**: Database khusus log. Menyimpan log dengan sangat efisien (karena hanya meng-indeks metadata/labelnya saja).
3. **Grafana**: UI Dashboard cantik tempat Anda mengetikkan *query* untuk mencari error.

## 📜 Structured JSON Logging
Kita menggunakan library `uber-go/zap` untuk mengeluarkan log dalam format JSON. Mengapa JSON?
Karena jika log berbentuk teks biasa: `Info: User login gagal`, komputer tidak paham strukturnya.
Dengan JSON: `{"level":"error", "msg":"Login gagal", "username":"johndoe", "trace_id":"123"}`
Grafana dapat memilah-milah log ini sehingga Anda bisa melakukan *query*: `Tampilkan semua error yang username-nya johndoe`.

## 🚀 Cara Menjalankan
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```
Lalu buka `http://localhost:3000` di peramban Anda.
