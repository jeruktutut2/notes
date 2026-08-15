-- Database schema for Saga Pattern Demo

CREATE TABLE IF NOT EXISTS inventory (
    item_id VARCHAR(50) PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL,
    stock INT NOT NULL CHECK (stock >= 0),
    reserved_stock INT DEFAULT 0 CHECK (reserved_stock >= 0),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(50) PRIMARY KEY,
    item_id VARCHAR(50) NOT NULL REFERENCES inventory(item_id),
    quantity INT NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL,
    status VARCHAR(30) NOT NULL, -- PENDING, COMPLETED, CANCELLED
    saga_type VARCHAR(50) NOT NULL, -- KAFKA_CHOREOGRAPHY, RABBITMQ_ORCHESTRATION
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payments (
    id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    status VARCHAR(30) NOT NULL, -- SUCCESS, FAILED, REFUNDED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS saga_logs (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    service_name VARCHAR(50) NOT NULL,
    step_name VARCHAR(50) NOT NULL,
    status VARCHAR(30) NOT NULL, -- EXECUTED, COMPENSATED, FAILED
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed initial data
INSERT INTO inventory (item_id, item_name, stock)
VALUES ('ITEM-001', 'MacBook Pro M3', 100)
ON CONFLICT (item_id) DO UPDATE SET stock = 100;
