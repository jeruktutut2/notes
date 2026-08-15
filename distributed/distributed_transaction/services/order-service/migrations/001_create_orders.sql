-- Migration: Create orders table
-- Order Service database schema

CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(36) PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    product_id VARCHAR(36) NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(15,2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    failure_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Status values:
-- PENDING              -> Order baru dibuat, menunggu inventory check
-- INVENTORY_RESERVED   -> Stok berhasil direserve, menunggu payment
-- PAYMENT_COMPLETED    -> Pembayaran berhasil, menunggu shipping
-- COMPLETED            -> Saga selesai, order berhasil
-- FAILED               -> Saga gagal, compensation sudah dijalankan

CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);
