# Distributed Tracing (OpenTelemetry & Jaeger)

Proyek ini mendemonstrasikan bagaimana kita bisa melacak perjalanan sebuah *request* saat ia melompat melintasi banyak layanan *Microservices*.

## 🕵️‍♂️ Mengapa Membutuhkan Distributed Tracing?
Di sistem arsitektur monolith (1 aplikasi besar), jika ada error atau *request* berjalan lambat, kita bisa dengan mudah melihat log atau *stacktrace* dari atas sampai bawah.

Namun di Microservices, 1 *request* pengguna (misal: "Checkout") bisa melewati:
- API Gateway
- Service Order
- Service Payment
- Service Inventory
- Service Notification

Jika prosesnya lambat, **Service manakah yang menyebabkan kelambatan?** Tanpa alat pelacak, mencarinya seperti mencari jarum di tumpukan jerami.

## 🔗 TraceID & Span
- **TraceID**: KTP unik (ID) untuk satu rentetan request dari awal hingga akhir. TraceID ini akan disuntikkan (*inject*) ke HTTP Header saat berpindah service, lalu disedot (*extract*) saat diterima.
- **Span**: Blok pekerjaan kecil (misal: query database, panggil fungsi tertentu) yang memiliki waktu *start* dan *end*.

## 🚀 Cara Menjalankan & Menguji
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```
Skrip akan menyalakan *Service A* dan *Service B*, serta server *Jaeger*.
1. *Service A* memanggil dirinya sendiri, lalu mengirim HTTP Request ke *Service B*.
2. OpenTelemetry akan otomatis menempelkan `trace_id` ke dalam HTTP Headers.
3. *Service B* mengambil `trace_id` tersebut dan melanjutkan pelacakan.
4. Semua data dikirim ke **Jaeger** di background.
5. Anda bisa membuka **http://localhost:16686** di browser untuk melihat UI visual grafik perjalanan request secara riil!
