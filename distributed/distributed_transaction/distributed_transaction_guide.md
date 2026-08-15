# Panduan Implementasi Distributed Transaction (Saga Pattern - 5 Services)

Panduan ini berisi langkah-langkah lengkap untuk membangun *distributed transaction* pada arsitektur microservices menggunakan tumpukan teknologi: **Golang (Echo Framework), PostgreSQL, Kafka, OpenTelemetry, dan Jaeger**. Kita akan menggunakan pendekatan **Saga Pattern (Choreography)** dengan melibatkan 5 services yang saling berkesinambungan.

**Skenario Alur Transaksi (Happy Path):**
1. **Order Service**: Membuat order pesanan (status `PENDING`).
2. **Inventory Service**: Mengecek dan memotong stok barang.
3. **Payment Service**: Mengecek dan memotong saldo user.
4. **Shipping Service**: Membuat jadwal resi/pengiriman barang.
5. **Notification Service**: Mengirim pesan (Email/SMS) ke pengguna bahwa pesanan sukses diproses.

**Alur Kompensasi (Rollback) Jika Gagal:**
*   Jika **Shipping Service gagal** (misalnya alamat tidak valid):
    *   Shipping menerbitkan event `ShippingFailed`.
    *   **Payment Service** menangkapnya -> mengembalikan saldo user.
    *   **Inventory Service** menangkapnya -> mengembalikan stok barang.
    *   **Order Service** menangkapnya -> mengubah pesanan menjadi `FAILED`.
    *   **Notification Service** menangkapnya -> mengirim email bahwa pesanan dibatalkan.

Gunakan file ini sebagai *checklist*. Ubah `[ ]` menjadi `[x]` jika langkah tersebut sudah diselesaikan.

---

## Tahap 1: Persiapan dan Setup Infrastruktur

- [ ] **1.1. Pahami Konsep Saga Pattern (5 Services)**
  - Pelajari *Saga Choreography* di mana *event* mengalir berantai dari satu servis ke servis lain.
  - Pahami kompleksitas *rollback* jika titik kegagalan ada di service ke-4 (Shipping), maka service 3, 2, dan 1 harus dikembalikan statusnya.

- [ ] **1.2. Buat `docker-compose.yml` untuk Infrastruktur**
  - Konfigurasi PostgreSQL dengan 4 database: `order_db`, `inventory_db`, `payment_db`, dan `shipping_db`. (Notification service tidak wajib pakai DB).
  - Konfigurasi Zookeeper & Kafka broker.
  - Konfigurasi Jaeger (All-in-one image).
  - Jalankan dengan `docker-compose up -d`.

- [ ] **1.3. Inisialisasi Project Repository**
  - Inisialisasi Go module.
  - Buat struktur direktori untuk 5 service: `cmd/order-service`, `cmd/inventory-service`, `cmd/payment-service`, `cmd/shipping-service`, `cmd/notification-service`.

---

## Tahap 2: Setup Core Packages (Shared Libraries)

- [ ] **2.1. Instalasi Dependencies**
  - Echo, GORM/pgx, Kafka-Go (Segmentio), dan OpenTelemetry.

- [ ] **2.2. Setup OpenTelemetry & Jaeger Exporter**
  - Buat fungsi `InitTracer` yang akan digunakan kelima service.

- [ ] **2.3. Setup Kafka Producer & Consumer Wrapper**
  - Fungsi publish/consume harus menyisipkan dan mengekstrak *Trace Context* di Kafka Headers.

---

## Tahap 3: Implementasi Service 1 (Order Service)

- [ ] **3.1. Setup Database & Model (Order)**
  - Model `Order` (ID, UserID, ProductID, Address, TotalAmount, Status: `PENDING`, `SUCCESS`, `FAILED`). DB: `order_db`.

- [ ] **3.2. Buat Endpoint `POST /orders`**
  - Simpan order dengan status `PENDING`.
  - **Publish Event**: `OrderCreated` ke topic `order-events` (beserta `TraceID`).

- [ ] **3.3. Buat Kafka Consumer untuk Kompensasi dan Status Final**
  - Listen topic: `shipping-events`, `payment-events`, `inventory-events`.
  - Jika event = `ShippingSuccess` -> update Order ke `SUCCESS`.
  - Jika event = `ShippingFailed`, `PaymentFailed`, atau `InventoryFailed` -> update Order ke `FAILED`.

---

## Tahap 4: Implementasi Service 2 (Inventory Service)

- [ ] **4.1. Setup Database & Model (Inventory)**
  - Model `Product` (ID, Stock). DB: `inventory_db`.

- [ ] **4.2. Buat Kafka Consumer (Reservasi Stok)**
  - Listen topic: `order-events`.
  - Saat ada `OrderCreated`: cek stok. 
  - Jika cukup: potong stok, **Publish** `InventoryReserved` ke topic `inventory-events`.
  - Jika kurang: **Publish** `InventoryFailed`.

- [ ] **4.3. Buat Kafka Consumer (Kompensasi Pengembalian Stok)**
  - Listen topic: `payment-events` dan `shipping-events`.
  - Jika ada `PaymentFailed` ATAU `ShippingFailed`: kembalikan stok barang yang sudah telanjur dipotong.

---

## Tahap 5: Implementasi Service 3 (Payment Service)

- [ ] **5.1. Setup Database & Model (Payment/Wallet)**
  - Model `Wallet` (UserID, Balance). DB: `payment_db`.

- [ ] **5.2. Buat Kafka Consumer (Proses Pembayaran)**
  - Listen topic: `inventory-events`.
  - Saat ada `InventoryReserved`: cek saldo.
  - Jika cukup: potong saldo, **Publish** `PaymentSuccess` ke topic `payment-events`.
  - Jika kurang: **Publish** `PaymentFailed`.

- [ ] **5.3. Buat Kafka Consumer (Kompensasi Pengembalian Saldo)**
  - Listen topic: `shipping-events`.
  - Jika ada `ShippingFailed`: kembalikan saldo user yang sudah dipotong (Refund).

---

## Tahap 6: Implementasi Service 4 (Shipping Service)

- [ ] **6.1. Setup Database & Model (Shipping)**
  - Model `Shipment` (ID, OrderID, Address, TrackingCode). DB: `shipping_db`.

- [ ] **6.2. Buat Kafka Consumer (Jadwalkan Pengiriman)**
  - Listen topic: `payment-events`.
  - Saat ada `PaymentSuccess`: validasi alamat (simulasi).
  - Jika alamat valid: generate Tracking Code, simpan ke DB, **Publish** `ShippingSuccess` ke topic `shipping-events`.
  - Jika alamat tidak valid/gagal: **Publish** `ShippingFailed`.

---

## Tahap 7: Implementasi Service 5 (Notification Service)

- [ ] **7.1. Setup OpenTelemetry & Dummy Mailer**
  - Tidak butuh database, hanya log ke console / integrasi SMTP/Twilio.

- [ ] **7.2. Buat Kafka Consumer (Penerima Hasil Akhir)**
  - Listen topic: `shipping-events`, `payment-events`, `inventory-events`.
  - Jika ada `ShippingSuccess`: Kirim email *"Pesanan Anda berhasil dan sedang dikirim dengan resi X"*.
  - Jika ada `ShippingFailed`, `PaymentFailed`, atau `InventoryFailed`: Kirim email *"Pesanan Anda dibatalkan karena suatu hal, saldo/stok (jika ada) telah dikembalikan"*.

---

## Tahap 8: Testing, Tracing & Observability

- [ ] **8.1. Jalankan Kelima Services**
  - Pastikan kelimanya berjalan dan terkoneksi ke Kafka & Jaeger.

- [ ] **8.2. Simulasi Transaksi Full Sukses**
  - Hit API Order.
  - Alur: `OrderCreated` -> `InventoryReserved` -> `PaymentSuccess` -> `ShippingSuccess`.
  - Verifikasi: Notifikasi sukses terkirim, status order SUCCESS.

- [ ] **8.3. Simulasi Transaksi Gagal di Akhir (Full Domino Compensation)**
  - Hit API Order dengan stok dan saldo cukup, TAPI berikan alamat "INVALID_ADDRESS" agar `Shipping Service` gagal.
  - Alur: `OrderCreated` -> `InventoryReserved` -> `PaymentSuccess` -> `ShippingFailed`.
  - Efek Domino Balik: 
    - `Payment Service` me-refund saldo.
    - `Inventory Service` mengembalikan stok.
    - `Order Service` mengubah pesanan FAILED.
    - `Notification Service` mengirim pesan gagal.

- [ ] **8.4. Verifikasi Tracing di Jaeger**
  - Trace span pada Jaeger akan sangat panjang dan indah. Anda bisa melihat lompatan HTTP Request -> Kafka dari ke-5 service tersebut dalam satu layar, mempermudah *debugging* jika ada service yang lambat (bottleneck) atau mati.
