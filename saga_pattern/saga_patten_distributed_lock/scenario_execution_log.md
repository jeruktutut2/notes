# Catatan Log Eksekusi Skenario (`scenario.sh`)

Dokumen ini berisi rekaman log eksekusi skrip pengujian [`scenario.sh`](file:///Users/bsa/Documents/por/saga_patten_distributed_lock/scenario.sh) yang mencakup alur pengujian **Saga Pattern** dan **Distributed Lock Watchdog Heartbeat**, serta kondisi Database (tabel `inventory` dan `orders`) sebelum dan sesudah setiap transaksi.

---

## 📋 Ringkasan Hasil Eksekusi

| Test Case | Deskripsi | Status | Hasil DB Orders |
| :--- | :--- | :---: | :--- |
| **Test Case 1** | Successful Saga Flow | `SUCCESS` | Order `ORD-41b0309d` dibuat dengan status `COMPLETED` |
| **Test Case 2** | Saga Rollback (Payment Failure) | `SUCCESS` | Order `ORD-3cf24c36` dibuat dengan status `CANCELLED_DUE_TO_PAYMENT_FAILURE` |
| **Test Case 3** | Distributed Lock Watchdog Heartbeat | `SUCCESS` | Distributed Lock diperpanjang 8s, request konkuren ditolak dengan status HTTP 423 `LOCKED` |

---

## 📜 Tangkapan Log Lengkap Eksekusi

```text
=======================================================
 1. STARTING SYSTEM CONTAINERS VIA DOCKER COMPOSE UP 
=======================================================
 Network saga_patten_distributed_lock_default Created 
 Container zookeeper_saga Created
 Container kafka_saga Created
 Container postgres_saga Created
 Container pgbouncer_saga Created
 Container redis_saga Created
 Container rabbitmq_saga Created
 Container app_saga Created

Waiting for services to become healthy and ready...
✔ Services are UP and healthy!

=======================================================
 2. TEST CASE 1: SUCCESSFUL SAGA FLOW 
=======================================================
-------------------------------------------------------
 DB STATE (BEFORE Test Case 1)
-------------------------------------------------------
Inventory Table:
 product_id | stock 
------------+-------
 PROD-101   |    50
(1 row)

Orders Table:
 id | product_id | quantity | total_price | status | created_at 
----+------------+----------+-------------+--------+------------
(0 rows)

-------------------------------------------------------
Sending request to create order (No simulation failure)...
Response:
{
  "order_id": "ORD-41b0309d",
  "status": "COMPLETED",
  "message": "Saga completed successfully: Order confirmed and processed"
}
Fetching Order Status from DB (via PgBouncer):
{
  "id": "ORD-41b0309d",
  "product_id": "PROD-101",
  "quantity": 2,
  "total_price": 150,
  "status": "COMPLETED",
  "created_at": "2026-08-07T06:46:10.818509Z"
}
-------------------------------------------------------
 DB STATE (AFTER Test Case 1)
-------------------------------------------------------
Inventory Table:
 product_id | stock 
------------+-------
 PROD-101   |    50
(1 row)

Orders Table:
      id      | product_id | quantity | total_price |  status   |         created_at         
--------------+------------+----------+-------------+-----------+----------------------------
 ORD-41b0309d | PROD-101   |        2 |      150.00 | COMPLETED | 2026-08-07 06:46:10.818509
(1 row)

-------------------------------------------------------

=======================================================
 3. TEST CASE 2: SAGA ROLLBACK (PAYMENT FAILURE) 
=======================================================
-------------------------------------------------------
 DB STATE (BEFORE Test Case 2)
-------------------------------------------------------
Inventory Table:
 product_id | stock 
------------+-------
 PROD-101   |    50
(1 row)

Orders Table:
      id      | product_id | quantity | total_price |  status   |         created_at         
--------------+------------+----------+-------------+-----------+----------------------------
 ORD-41b0309d | PROD-101   |        2 |      150.00 | COMPLETED | 2026-08-07 06:46:10.818509
(1 row)

-------------------------------------------------------
Sending request to create order with simulated PAYMENT failure...
Response:
{
  "order_id": "ORD-3cf24c36",
  "status": "CANCELLED_DUE_TO_PAYMENT_FAILURE",
  "message": "Saga rolled back: Payment failed, inventory released"
}
Fetching Order Status from DB (Verifying Compensating Rollback):
{
  "id": "ORD-3cf24c36",
  "product_id": "PROD-101",
  "quantity": 1,
  "total_price": 75,
  "status": "CANCELLED_DUE_TO_PAYMENT_FAILURE",
  "created_at": "2026-08-07T06:46:11.025698Z"
}
-------------------------------------------------------
 DB STATE (AFTER Test Case 2)
-------------------------------------------------------
Inventory Table:
 product_id | stock 
------------+-------
 PROD-101   |    50
(1 row)

Orders Table:
      id      | product_id | quantity | total_price |              status              |         created_at         
--------------+------------+----------+-------------+----------------------------------+----------------------------
 ORD-41b0309d | PROD-101   |        2 |      150.00 | COMPLETED                        | 2026-08-07 06:46:10.818509
 ORD-3cf24c36 | PROD-101   |        1 |       75.00 | CANCELLED_DUE_TO_PAYMENT_FAILURE | 2026-08-07 06:46:11.025698
(2 rows)

-------------------------------------------------------

=======================================================
 4. TEST CASE 3: DISTRIBUTED LOCK WATCHDOG HEARTBEAT 
=======================================================
-------------------------------------------------------
 DB STATE (BEFORE Test Case 3)
-------------------------------------------------------
Inventory Table:
 product_id | stock 
------------+-------
 PROD-101   |    50
(1 row)

Orders Table:
      id      | product_id | quantity | total_price |              status              |         created_at         
--------------+------------+----------+-------------+----------------------------------+----------------------------
 ORD-41b0309d | PROD-101   |        2 |      150.00 | COMPLETED                        | 2026-08-07 06:46:10.818509
 ORD-3cf24c36 | PROD-101   |        1 |       75.00 | CANCELLED_DUE_TO_PAYMENT_FAILURE | 2026-08-07 06:46:11.025698
(2 rows)

-------------------------------------------------------
Triggering 8-second long critical task holding lock with 3s initial TTL...
Background Watchdog Heartbeat will extend TTL every 1s continuously.
Attempting concurrent request to the same locked resource...
Concurrent Request Response (Expected 423 Locked):
{
  "lockKey": "demo:critical-resource",
  "message": "Resource is currently locked by Watchdog. Try again after the processing finishes.",
  "status": "LOCKED"
}
First Task Response:
{
  "heldDuration": "8s",
  "lockKey": "demo:critical-resource",
  "message": "Critical section executed safely. Distributed Lock Watchdog renewed lock continuously.",
  "status": "SUCCESS"
}
-------------------------------------------------------
 DB STATE (AFTER Test Case 3 / FINAL)
-------------------------------------------------------
Inventory Table:
 product_id | stock 
------------+-------
 PROD-101   |    50
(1 row)

Orders Table:
      id      | product_id | quantity | total_price |              status              |         created_at         
--------------+------------+----------+-------------+----------------------------------+----------------------------
 ORD-41b0309d | PROD-101   |        2 |      150.00 | COMPLETED                        | 2026-08-07 06:46:10.818509
 ORD-3cf24c36 | PROD-101   |        1 |       75.00 | CANCELLED_DUE_TO_PAYMENT_FAILURE | 2026-08-07 06:46:11.025698
(2 rows)

-------------------------------------------------------

=======================================================
 5. STOPPING SYSTEM CONTAINERS VIA DOCKER COMPOSE DOWN 
=======================================================
 Container app_saga Stopped & Removed
 Container pgbouncer_saga Stopped & Removed
 Container postgres_saga Stopped & Removed
 Container redis_saga Stopped & Removed
 Container kafka_saga Stopped & Removed
 Container rabbitmq_saga Stopped & Removed
 Container zookeeper_saga Stopped & Removed
 Network saga_patten_distributed_lock_default Removed
=======================================================
 SCRIPT EXECUTED SUCCESSFULLY! 
=======================================================
```
