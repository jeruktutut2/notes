# Saga Pattern Demo - Scenario Execution Logs

**Waktu Eksekusi**: 8 Agustus 2026  
**Status**: Semua Skenario Berhasil (`ALL SAGA SCENARIOS COMPLETED`)

---

## 📋 Ringkasan Hasil Skenario

| Skenario | Pola Saga | Deskripsi | Status Order | Stok Awal | Stok Akhir | Result |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Skenario 1** | Kafka Choreography | Happy Path (Sukses) | `COMPLETED` | 100 | 98 (-2) | `PASSED` |
| **Skenario 2** | Kafka Choreography | Rollback (Gagal Bayar) | `CANCELLED` | 98 | 98 (Kembali) | `PASSED` |
| **Skenario 3** | RabbitMQ Orchestration | Happy Path (Sukses) | `COMPLETED` | 98 | 93 (-5) | `PASSED` |
| **Skenario 4** | RabbitMQ Orchestration | Rollback (Gagal Bayar) | `CANCELLED` | 93 | 93 (Kembali) | `PASSED` |

---

## 📜 Full Console Execution Log

```text
========================================================================
             SAGA PATTERN DEMO - AUTOMATED TEST SCENARIOS               
========================================================================
Starting Docker Compose services...
Waiting for Kafka Choreography Service to be ready at http://localhost:8081/health... READY!
Waiting for RabbitMQ Orchestration Service to be ready at http://localhost:8082/health... READY!
Allowing services and background consumers to settle...

--- Initial Inventory State (from DB) ---
 item_id  |   item_name    | stock | reserved_stock |         updated_at         
----------+----------------+-------+----------------+----------------------------
 ITEM-001 | MacBook Pro M3 |   100 |              0 | 2026-08-08 02:53:40.233475
(1 row)


========================================================================
 SCENARIO 1: Kafka Choreography - Happy Path (Success)                 
========================================================================
Product Data Before Transaction (from DB):
 item_id  |   item_name    | stock | reserved_stock |         updated_at         
----------+----------------+-------+----------------+----------------------------
 ITEM-001 | MacBook Pro M3 |   100 |              0 | 2026-08-08 02:53:40.233475
(1 row)

Order Created: ORD-KAFKA-78537ec5
Waiting for event propagation across Kafka topics...
Final Order Details (via API):
{
  "item_id": "ITEM-001",
  "order_id": "ORD-KAFKA-78537ec5",
  "quantity": 2,
  "saga_logs": [
    {
      "created_at": "2026-08-08T02:53:49.377416Z",
      "details": "Order created in database",
      "service": "OrderService",
      "status": "PENDING",
      "step": "CreateOrder"
    },
    {
      "created_at": "2026-08-08T02:53:50.412651Z",
      "details": "Deducted 2 units",
      "service": "InventoryService",
      "status": "EXECUTED",
      "step": "DeductStock"
    },
    {
      "created_at": "2026-08-08T02:53:51.429736Z",
      "details": "Payment charged successfully",
      "service": "PaymentService",
      "status": "EXECUTED",
      "step": "ProcessPayment"
    },
    {
      "created_at": "2026-08-08T02:53:52.444094Z",
      "details": "Order status updated to COMPLETED",
      "service": "OrderService",
      "status": "EXECUTED",
      "step": "FinalizeOrder"
    }
  ],
  "saga_type": "KAFKA_CHOREOGRAPHY",
  "status": "COMPLETED",
  "total_amount": 150000
}
DB Records for Transaction ORD-KAFKA-78537ec5:
[orders table]
         id         | item_id  | quantity | total_amount |  status   |     saga_type      
--------------------+----------+----------+--------------+-----------+--------------------
 ORD-KAFKA-78537ec5 | ITEM-001 |        2 |    150000.00 | COMPLETED | KAFKA_CHOREOGRAPHY
(1 row)

[payments table]
      id      |      order_id      |  amount   | status  
--------------+--------------------+-----------+---------
 PAY-5c1b27fa | ORD-KAFKA-78537ec5 | 150000.00 | SUCCESS
(1 row)

[saga_logs table]
 id |   service_name   |   step_name    |  status  |              details              
----+------------------+----------------+----------+-----------------------------------
  1 | OrderService     | CreateOrder    | PENDING  | Order created in database
  2 | InventoryService | DeductStock    | EXECUTED | Deducted 2 units
  3 | PaymentService   | ProcessPayment | EXECUTED | Payment charged successfully
  4 | OrderService     | FinalizeOrder  | EXECUTED | Order status updated to COMPLETED
(4 rows)

Product Data After Transaction (from DB):
 item_id  |   item_name    | stock | reserved_stock |         updated_at         
----------+----------------+-------+----------------+----------------------------
 ITEM-001 | MacBook Pro M3 |    98 |              0 | 2026-08-08 02:53:50.410922
(1 row)

✓ SCENARIO 1 PASSED: Order status is COMPLETED

========================================================================
 SCENARIO 2: Kafka Choreography - Rollback (Payment Failure)          
========================================================================
Product Data Before Transaction (from DB):
 item_id  |   item_name    | stock | reserved_stock |         updated_at         
----------+----------------+-------+----------------+----------------------------
 ITEM-001 | MacBook Pro M3 |    98 |              0 | 2026-08-08 02:53:50.410922
(1 row)

Order Created (Configured to Fail Payment): ORD-KAFKA-d4565332
Waiting for compensation events...
Final Order Details (via API):
{
  "item_id": "ITEM-001",
  "order_id": "ORD-KAFKA-d4565332",
  "quantity": 3,
  "saga_logs": [
    {
      "created_at": "2026-08-08T02:53:56.749747Z",
      "details": "Order created in database",
      "service": "OrderService",
      "status": "PENDING",
      "step": "CreateOrder"
    },
    {
      "created_at": "2026-08-08T02:53:57.76165Z",
      "details": "Deducted 3 units",
      "service": "InventoryService",
      "status": "EXECUTED",
      "step": "DeductStock"
    },
    {
      "created_at": "2026-08-08T02:53:58.774802Z",
      "details": "Payment rejected by gateway rule",
      "service": "PaymentService",
      "status": "FAILED",
      "step": "ProcessPayment"
    },
    {
      "created_at": "2026-08-08T02:53:59.790172Z",
      "details": "Order status updated to CANCELLED due to Payment Failure",
      "service": "OrderService",
      "status": "COMPENSATED",
      "step": "FinalizeOrder"
    }
  ],
  "saga_type": "KAFKA_CHOREOGRAPHY",
  "status": "CANCELLED",
  "total_amount": 200000
}
DB Records for Transaction ORD-KAFKA-d4565332:
[orders table]
         id         | item_id  | quantity | total_amount |  status   |     saga_type      
--------------------+----------+----------+--------------+-----------+--------------------
 ORD-KAFKA-d4565332 | ITEM-001 |        3 |    200000.00 | CANCELLED | KAFKA_CHOREOGRAPHY
(1 row)

[payments table]
      id      |      order_id      |  amount   | status 
--------------+--------------------+-----------+--------
 PAY-98df5b25 | ORD-KAFKA-d4565332 | 200000.00 | FAILED
(1 row)

[saga_logs table]
 id |   service_name   |   step_name    |   status    |                         details                          
----+------------------+----------------+-------------+----------------------------------------------------------
  5 | OrderService     | CreateOrder    | PENDING     | Order created in database
  6 | InventoryService | DeductStock    | EXECUTED    | Deducted 3 units
  7 | PaymentService   | ProcessPayment | FAILED      | Payment rejected by gateway rule
  8 | OrderService     | FinalizeOrder  | COMPENSATED | Order status updated to CANCELLED due to Payment Failure
(4 rows)

Product Data After Transaction (from DB):
 item_id  |   item_name    | stock | reserved_stock |         updated_at         
----------+----------------+-------+----------------+----------------------------
 ITEM-001 | MacBook Pro M3 |    98 |              0 | 2026-08-08 02:53:59.787419
(1 row)

✓ SCENARIO 2 PASSED: Order status is CANCELLED and stock restored!

========================================================================
 SCENARIO 3: RabbitMQ Orchestration - Happy Path (Success)            
========================================================================
Product Data Before Transaction (from DB):
 item_id  |   item_name    | stock | reserved_stock |         updated_at         
----------+----------------+-------+----------------+----------------------------
 ITEM-001 | MacBook Pro M3 |    98 |              0 | 2026-08-08 02:53:59.787419
(1 row)

Order Created: ORD-RMQ-fc8592e9
Waiting for orchestrator commands via RabbitMQ...
Final Order Details (via API):
{
  "item_id": "ITEM-001",
  "order_id": "ORD-RMQ-fc8592e9",
  "quantity": 5,
  "saga_logs": [
    {
      "created_at": "2026-08-08T02:54:04.056002Z",
      "details": "Saga Orchestration started",
      "service": "OrchestratorService",
      "status": "PENDING",
      "step": "StartSaga"
    },
    {
      "created_at": "2026-08-08T02:54:04.0565Z",
      "details": "Sent ReserveInventoryCommand to RabbitMQ",
      "service": "OrchestratorService",
      "status": "EXECUTED",
      "step": "SendCommand"
    },
    {
      "created_at": "2026-08-08T02:54:04.058388Z",
      "details": "Reserved 5 units",
      "service": "InventoryWorker",
      "status": "EXECUTED",
      "step": "DeductStock"
    },
    {
      "created_at": "2026-08-08T02:54:04.059224Z",
      "details": "Sent ProcessPaymentCommand to RabbitMQ",
      "service": "OrchestratorService",
      "status": "EXECUTED",
      "step": "ProcessPaymentCommand"
    },
    {
      "created_at": "2026-08-08T02:54:04.06027Z",
      "details": "Payment processed successfully",
      "service": "PaymentWorker",
      "status": "EXECUTED",
      "step": "ProcessPayment"
    },
    {
      "created_at": "2026-08-08T02:54:04.061214Z",
      "details": "Saga completed successfully",
      "service": "OrchestratorService",
      "status": "EXECUTED",
      "step": "FinalizeSaga"
    }
  ],
  "saga_type": "RABBITMQ_ORCHESTRATION",
  "status": "COMPLETED",
  "total_amount": 300000
}
DB Records for Transaction ORD-RMQ-fc8592e9:
[orders table]
        id        | item_id  | quantity | total_amount |  status   |       saga_type        
------------------+----------+----------+--------------+-----------+------------------------
 ORD-RMQ-fc8592e9 | ITEM-001 |        5 |    300000.00 | COMPLETED | RABBITMQ_ORCHESTRATION
(1 row)

[payments table]
        id        |     order_id     |  amount   | status  
------------------+------------------+-----------+---------
 PAY-RMQ-39f5d06f | ORD-RMQ-fc8592e9 | 300000.00 | SUCCESS
(1 row)

[saga_logs table]
 id |    service_name     |       step_name       |  status  |                 details                  
----+---------------------+-----------------------+----------+------------------------------------------
  9 | OrchestratorService | StartSaga             | PENDING  | Saga Orchestration started
 10 | OrchestratorService | SendCommand           | EXECUTED | Sent ReserveInventoryCommand to RabbitMQ
 11 | InventoryWorker     | DeductStock           | EXECUTED | Reserved 5 units
 12 | OrchestratorService | ProcessPaymentCommand | EXECUTED | Sent ProcessPaymentCommand to RabbitMQ
 13 | PaymentWorker       | ProcessPayment        | EXECUTED | Payment processed successfully
 14 | OrchestratorService | FinalizeSaga          | EXECUTED | Saga completed successfully
(6 rows)

Product Data After Transaction (from DB):
 item_id  |   item_name    | stock | reserved_stock |         updated_at         
----------+----------------+-------+----------------+----------------------------
 ITEM-001 | MacBook Pro M3 |    93 |              0 | 2026-08-08 02:54:04.057318
(1 row)

✓ SCENARIO 3 PASSED: Order status is COMPLETED

========================================================================
 SCENARIO 4: RabbitMQ Orchestration - Rollback (Payment Failure)       
========================================================================
Product Data Before Transaction (from DB):
 item_id  |   item_name    | stock | reserved_stock |         updated_at         
----------+----------------+-------+----------------+----------------------------
 ITEM-001 | MacBook Pro M3 |    93 |              0 | 2026-08-08 02:54:04.057318
(1 row)

Order Created (Configured to Fail Payment): ORD-RMQ-e8364a6c
Waiting for orchestrator to execute compensation steps...
Final Order Details (via API):
{
  "item_id": "ITEM-001",
  "order_id": "ORD-RMQ-e8364a6c",
  "quantity": 4,
  "saga_logs": [
    {
      "created_at": "2026-08-08T02:54:07.390123Z",
      "details": "Saga Orchestration started",
      "service": "OrchestratorService",
      "status": "PENDING",
      "step": "StartSaga"
    },
    {
      "created_at": "2026-08-08T02:54:07.390603Z",
      "details": "Sent ReserveInventoryCommand to RabbitMQ",
      "service": "OrchestratorService",
      "status": "EXECUTED",
      "step": "SendCommand"
    },
    {
      "created_at": "2026-08-08T02:54:07.391884Z",
      "details": "Reserved 4 units",
      "service": "InventoryWorker",
      "status": "EXECUTED",
      "step": "DeductStock"
    },
    {
      "created_at": "2026-08-08T02:54:07.392606Z",
      "details": "Sent ProcessPaymentCommand to RabbitMQ",
      "service": "OrchestratorService",
      "status": "EXECUTED",
      "step": "ProcessPaymentCommand"
    },
    {
      "created_at": "2026-08-08T02:54:07.393173Z",
      "details": "Payment rejected by mock rule",
      "service": "PaymentWorker",
      "status": "FAILED",
      "step": "ProcessPayment"
    },
    {
      "created_at": "2026-08-08T02:54:07.393742Z",
      "details": "Payment failed. Sending CompensateInventoryCommand",
      "service": "OrchestratorService",
      "status": "FAILED",
      "step": "TriggerCompensation"
    },
    {
      "created_at": "2026-08-08T02:54:07.394421Z",
      "details": "Saga cancelled and compensation executed",
      "service": "OrchestratorService",
      "status": "COMPENSATED",
      "step": "FinalizeSaga"
    },
    {
      "created_at": "2026-08-08T02:54:07.395088Z",
      "details": "Restored 4 units",
      "service": "InventoryWorker",
      "status": "COMPENSATED",
      "step": "RestoreStock"
    }
  ],
  "saga_type": "RABBITMQ_ORCHESTRATION",
  "status": "CANCELLED",
  "total_amount": 250000
}
DB Records for Transaction ORD-RMQ-e8364a6c:
[orders table]
        id        | item_id  | quantity | total_amount |  status   |       saga_type        
------------------+----------+----------+--------------+-----------+------------------------
 ORD-RMQ-e8364a6c | ITEM-001 |        4 |    250000.00 | CANCELLED | RABBITMQ_ORCHESTRATION
(1 row)

[payments table]
        id        |     order_id     |  amount   | status 
------------------+------------------+-----------+--------
 PAY-RMQ-9799624e | ORD-RMQ-e8364a6c | 250000.00 | FAILED
(1 row)

[saga_logs table]
 id |    service_name     |       step_name       |   status    |                      details                       
----+---------------------+-----------------------+-------------+----------------------------------------------------
 15 | OrchestratorService | StartSaga             | PENDING     | Saga Orchestration started
 16 | OrchestratorService | SendCommand           | EXECUTED    | Sent ReserveInventoryCommand to RabbitMQ
 17 | InventoryWorker     | DeductStock           | EXECUTED    | Reserved 4 units
 18 | OrchestratorService | ProcessPaymentCommand | EXECUTED    | Sent ProcessPaymentCommand to RabbitMQ
 19 | PaymentWorker       | ProcessPayment        | FAILED      | Payment rejected by mock rule
 20 | OrchestratorService | TriggerCompensation   | FAILED      | Payment failed. Sending CompensateInventoryCommand
 21 | OrchestratorService | FinalizeSaga          | COMPENSATED | Saga cancelled and compensation executed
 22 | InventoryWorker     | RestoreStock          | COMPENSATED | Restored 4 units
(8 rows)

Product Data After Transaction (from DB):
 item_id  |   item_name    | stock | reserved_stock |         updated_at         
----------+----------------+-------+----------------+----------------------------
 ITEM-001 | MacBook Pro M3 |    93 |              0 | 2026-08-08 02:54:07.394164
(1 row)

✓ SCENARIO 4 PASSED: Order status is CANCELLED and stock restored!

--- Final All Orders Summary (from DB) ---
         id         | item_id  | quantity | total_amount |  status   |       saga_type        
--------------------+----------+----------+--------------+-----------+------------------------
 ORD-KAFKA-78537ec5 | ITEM-001 |        2 |    150000.00 | COMPLETED | KAFKA_CHOREOGRAPHY
 ORD-KAFKA-d4565332 | ITEM-001 |        3 |    200000.00 | CANCELLED | KAFKA_CHOREOGRAPHY
 ORD-RMQ-fc8592e9   | ITEM-001 |        5 |    300000.00 | COMPLETED | RABBITMQ_ORCHESTRATION
 ORD-RMQ-e8364a6c   | ITEM-001 |        4 |    250000.00 | CANCELLED | RABBITMQ_ORCHESTRATION
(4 rows)


--- Final Inventory State (from DB) ---
 item_id  |   item_name    | stock | reserved_stock |         updated_at         
----------+----------------+-------+----------------+----------------------------
 ITEM-001 | MacBook Pro M3 |    93 |              0 | 2026-08-08 02:54:07.394164
(1 row)


========================================================================
                     ALL SAGA SCENARIOS COMPLETED!                      
========================================================================
```
