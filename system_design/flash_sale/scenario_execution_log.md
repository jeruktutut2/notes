# 📜 Flash Sale System Design - Scenario Execution Log

Execution Timestamp: 2026-08-07 15:10:01
Architecture Layers: Kong Gateway | Go Echo Services | Rust Axum Services | PgBouncer | Postgres | Redis | Kafka

---
## 1. Skenario 1: Pre-Sale Setup & Inventory Pre-heating

Mengaktifkan Flash Sale event dan memuat stok awal (5 unit) ke Redis Instance via API Gateway.

#### 🔍 DB State Snapshot: BEFORE Pre-Heating (PostgreSQL flash_sales)
```sql
SELECT id, product_id, sale_price, original_stock, remaining_stock, status FROM flash_sales WHERE id = '44444444-4444-4444-4444-444444444444';
```
```text
                  id                  |              product_id              | sale_price | original_stock | remaining_stock | status 
--------------------------------------+--------------------------------------+------------+----------------+-----------------+--------
 44444444-4444-4444-4444-444444444444 | 11111111-1111-1111-1111-111111111111 | 5000000.00 |              5 |               5 | ACTIVE
(1 row)

```

Executing Preheat API Request...
```json
{"flash_sale_id":"44444444-4444-4444-4444-444444444444","message":"Stock pre-heated to Redis successfully","status_set":"ACTIVE","stock_loaded":5}
```

#### 🔍 DB State Snapshot: AFTER Pre-Heating (PostgreSQL flash_sales)
```sql
SELECT id, product_id, sale_price, original_stock, remaining_stock, status FROM flash_sales WHERE id = '44444444-4444-4444-4444-444444444444';
```
```text
                  id                  |              product_id              | sale_price | original_stock | remaining_stock | status 
--------------------------------------+--------------------------------------+------------+----------------+-----------------+--------
 44444444-4444-4444-4444-444444444444 | 11111111-1111-1111-1111-111111111111 | 5000000.00 |              5 |               5 | ACTIVE
(1 row)

```

## 2. Skenario 2: Successful Flash Sale Purchase Flow (User 1 - Budi)

User 1 mengirim request transaksi pembelian. Service Go (Echo) memotong stok via Atomic Redis Lua script dan memasukkan event ke Kafka.

#### 🔍 DB State Snapshot: BEFORE Purchase (PostgreSQL orders)
```sql
SELECT id, user_id, flash_sale_id, price, status, idempotency_key, created_at FROM orders WHERE user_id = '22222222-2222-2222-2222-222222222222';
```
```text
 id | user_id | flash_sale_id | price | status | idempotency_key | created_at 
----+---------+---------------+-------+--------+-----------------+------------
(0 rows)

```

HTTP Response (202 Accepted):
```json
{"data":{"message":"Pesanan Anda sedang diproses","order_id":"60e575b5-8c41-4f31-9651-2521036b4cb7","payment_deadline":"2026-08-07T07:25:03.1084203Z","remaining_stock":4,"status":"PENDING"},"status":"success"}
```

Waiting 3 seconds for Kafka Consumer (Order Service Go) to persist order to PostgreSQL via PgBouncer...
#### 🔍 DB State Snapshot: AFTER Purchase & Kafka Consumption (PostgreSQL orders)
```sql
SELECT id, user_id, flash_sale_id, price, status, idempotency_key, created_at FROM orders WHERE user_id = '22222222-2222-2222-2222-222222222222';
```
```text
                  id                  |               user_id                |            flash_sale_id             |   price    |      status      | idempotency_key  |          created_at           
--------------------------------------+--------------------------------------+--------------------------------------+------------+------------------+------------------+-------------------------------
 60e575b5-8c41-4f31-9651-2521036b4cb7 | 22222222-2222-2222-2222-222222222222 | 44444444-4444-4444-4444-444444444444 | 5000000.00 | AWAITING_PAYMENT | idemp_user1_tx01 | 2026-08-07 07:10:03.133153+00
(1 row)

```

## 3. Skenario 3: Duplicate Purchase Prevention (User 1 Try Again)

User 1 mencoba menekan tombol 'Beli' dua kali. Redis SISMEMBER memblokir request kedua untuk mencegah double purchase.

#### 🔍 DB State Snapshot: BEFORE Duplicate Attempt (PostgreSQL order count for User 1)
```sql
SELECT COUNT(*) AS user1_order_count FROM orders WHERE user_id = '22222222-2222-2222-2222-222222222222';
```
```text
 user1_order_count 
-------------------
                 1
(1 row)

```

HTTP Response (409 Conflict):
```json
{"error":{"code":"ALREADY_PURCHASED","message":"Anda sudah membeli produk ini"},"status":"error"}
```

#### 🔍 DB State Snapshot: AFTER Duplicate Attempt (PostgreSQL order count for User 1)
```sql
SELECT COUNT(*) AS user1_order_count FROM orders WHERE user_id = '22222222-2222-2222-2222-222222222222';
```
```text
 user1_order_count 
-------------------
                 1
(1 row)

```

## 4. Skenario 4: Stock Depletion & Sold Out Prevention

Menghabiskan sisa 4 unit stok hingga mencapai 0, lalu menguji request setelah SOLD OUT.

#### 🔍 DB State Snapshot: BEFORE Stock Depletion (PostgreSQL orders summary)
```sql
SELECT status, COUNT(*) FROM orders GROUP BY status;
```
```text
      status      | count 
------------------+-------
 AWAITING_PAYMENT |     1
(1 row)

```

Attempting purchase after stock is 0 (Expect 410 Gone):
```json
{"error":{"code":"SALE_NOT_ACTIVE","message":"Flash Sale belum dimulai atau sudah berakhir"},"status":"error"}
```

#### 🔍 DB State Snapshot: AFTER Stock Depletion (PostgreSQL orders summary - Max 5 active orders)
```sql
SELECT status, COUNT(*) FROM orders GROUP BY status;
```
```text
      status      | count 
------------------+-------
 AWAITING_PAYMENT |     5
(1 row)

```

## 5. Skenario 5: Successful Payment Processing

User 1 menyelesaikan pembayaran via Payment Service Go (Echo). Status order diubah ke PAID dan entry dibuat di tabel payments.

#### 🔍 DB State Snapshot: BEFORE Payment (PostgreSQL order & payments for Order 60e575b5-8c41-4f31-9651-2521036b4cb7)
```sql
SELECT id, status, price FROM orders WHERE id = '60e575b5-8c41-4f31-9651-2521036b4cb7'; SELECT * FROM payments WHERE order_id = '60e575b5-8c41-4f31-9651-2521036b4cb7';
```
```text
                  id                  |      status      |   price    
--------------------------------------+------------------+------------
 60e575b5-8c41-4f31-9651-2521036b4cb7 | AWAITING_PAYMENT | 5000000.00
(1 row)

 id | order_id | amount | payment_method | gateway_ref_id | status | paid_at | created_at 
----+----------+--------+----------------+----------------+--------+---------+------------
(0 rows)

```

HTTP Payment Response:
```json
{"gateway_ref_id":"PAY-64a8110a","message":"Pembayaran berhasil","order_id":"60e575b5-8c41-4f31-9651-2521036b4cb7","payment_id":"46b517b4-bad8-4974-8f17-4a42184d1cb8","status":"SUCCESS"}
```

#### 🔍 DB State Snapshot: AFTER Payment (PostgreSQL order & payments for Order 60e575b5-8c41-4f31-9651-2521036b4cb7)
```sql
SELECT id, status, price, updated_at FROM orders WHERE id = '60e575b5-8c41-4f31-9651-2521036b4cb7'; SELECT id, order_id, amount, payment_method, gateway_ref_id, status, paid_at FROM payments WHERE order_id = '60e575b5-8c41-4f31-9651-2521036b4cb7';
```
```text
                  id                  | status |   price    |          updated_at           
--------------------------------------+--------+------------+-------------------------------
 60e575b5-8c41-4f31-9651-2521036b4cb7 | PAID   | 5000000.00 | 2026-08-07 07:10:14.115309+00
(1 row)

                  id                  |               order_id               |   amount   | payment_method | gateway_ref_id | status  |            paid_at            
--------------------------------------+--------------------------------------+------------+----------------+----------------+---------+-------------------------------
 46b517b4-bad8-4974-8f17-4a42184d1cb8 | 60e575b5-8c41-4f31-9651-2521036b4cb7 | 5000000.00 | E_WALLET       | PAY-64a8110a   | SUCCESS | 2026-08-07 07:10:14.115309+00
(1 row)

```

## 6. Skenario 6: Payment Failure & Redis Stock Restoration

User 2 melakukan order saat stok tersedia, namun pembayaran gagal. Payment Service mengubah status ke PAYMENT_FAILED dan memanggil Redis Lua script restore_stock.lua untuk mengembalikan 1 unit stok ke Redis.

#### 🔍 DB State Snapshot: BEFORE Payment Failure (PostgreSQL orders & payments for User 2)
```sql
SELECT id, user_id, status FROM orders WHERE id = 'cdab56eb-5bce-41a3-bf56-a64aa738b558';
```
```text
                  id                  |               user_id                |      status      
--------------------------------------+--------------------------------------+------------------
 cdab56eb-5bce-41a3-bf56-a64aa738b558 | 33333333-3333-3333-3333-333333333333 | AWAITING_PAYMENT
(1 row)

```

HTTP Payment Failure Response:
```json
{"message":"Pembayaran gagal, stok telah dikembalikan","order_id":"cdab56eb-5bce-41a3-bf56-a64aa738b558","restored_stock":5,"status":"PAYMENT_FAILED"}
```

#### 🔍 DB State Snapshot: AFTER Payment Failure & Stock Restoration (PostgreSQL orders & payments for User 2)
```sql
SELECT id, user_id, status FROM orders WHERE id = 'cdab56eb-5bce-41a3-bf56-a64aa738b558'; SELECT id, order_id, status FROM payments WHERE order_id = 'cdab56eb-5bce-41a3-bf56-a64aa738b558';
```
```text
                  id                  |               user_id                |     status     
--------------------------------------+--------------------------------------+----------------
 cdab56eb-5bce-41a3-bf56-a64aa738b558 | 33333333-3333-3333-3333-333333333333 | PAYMENT_FAILED
(1 row)

                  id                  |               order_id               | status 
--------------------------------------+--------------------------------------+--------
 c4d50947-cb80-4cad-a764-afd1cd449805 | cdab56eb-5bce-41a3-bf56-a64aa738b558 | FAILED
(1 row)

```

## 7. Skenario 7: Rust Inventory Service Post-Sale Reconciliation

Service Rust (Axum) memeriksa konsistensi antara jumlah order terbayar di PostgreSQL via PgBouncer dengan stok di Redis.

```json
{"service":"inventory_service (Rust/Axum)","flash_sale_id":"44444444-4444-4444-4444-444444444444","redis_stock":5,"db_orders":0,"total_accounted":5,"original_stock":5,"is_balanced":true,"discrepancy":0,"message":"RECONCILIATION SUCCESSFUL: Zero discrepancy detected between Redis stock and PostgreSQL orders."}
```

