-- Migration: Create products and inventory_logs tables
-- Inventory Service database schema

CREATE TABLE IF NOT EXISTS products (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    reserved_stock INT NOT NULL DEFAULT 0,
    price DECIMAL(15,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Log semua perubahan inventory untuk audit trail
CREATE TABLE IF NOT EXISTS inventory_logs (
    id VARCHAR(36) PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL,
    product_id VARCHAR(36) NOT NULL,
    quantity INT NOT NULL,
    action VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Action values: RESERVE, RELEASE, DEDUCT

CREATE INDEX idx_inventory_logs_order_id ON inventory_logs(order_id);
CREATE INDEX idx_inventory_logs_product_id ON inventory_logs(product_id);

-- Seed data: produk awal untuk testing
INSERT INTO products (id, name, stock, reserved_stock, price) VALUES
    ('prod-001', 'Laptop Gaming', 50, 0, 15000000),
    ('prod-002', 'Mechanical Keyboard', 100, 0, 1500000),
    ('prod-003', 'Gaming Mouse', 200, 0, 750000),
    ('prod-004', 'Monitor 4K', 30, 0, 5000000),
    ('prod-005', 'Headset Wireless', 75, 0, 2000000);
