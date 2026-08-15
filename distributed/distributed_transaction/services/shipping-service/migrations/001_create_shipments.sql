-- Migration: Create shipments table
-- Shipping Service database schema

CREATE TABLE IF NOT EXISTS shipments (
    id VARCHAR(36) PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL,
    address VARCHAR(500) NOT NULL DEFAULT 'Default Address',
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    tracking_number VARCHAR(100),
    failure_reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Status values:
-- PENDING    -> Shipment sedang diproses
-- CREATED    -> Shipment berhasil dibuat
-- FAILED     -> Shipment gagal
-- CANCELLED  -> Shipment dibatalkan (compensation)

CREATE INDEX idx_shipments_order_id ON shipments(order_id);
CREATE INDEX idx_shipments_status ON shipments(status);
