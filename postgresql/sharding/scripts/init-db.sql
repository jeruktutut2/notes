-- Enable Citus extension (pre-installed in citusdata/citus image)
CREATE EXTENSION IF NOT EXISTS citus;

-- Ensure coordinator hostname is registered
SELECT citus_set_coordinator_host('coordinator', 5432);

-- Create Distributed Tables Example
-- Table 1: Users (Sharded by id)
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Orders (Sharded by user_id for co-location with users)
CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL,
    user_id BIGINT NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    status VARCHAR(30) DEFAULT 'completed',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, id)
);

-- Table 3: Reference Table (Replicated on all worker nodes for fast JOINs)
CREATE TABLE IF NOT EXISTS product_categories (
    id INT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT
);


-- Populate reference table initial data
INSERT INTO product_categories (id, category_name, description) VALUES
(1, 'Electronics', 'Gadgets and electronic components'),
(2, 'Clothing', 'Apparel and accessories'),
(3, 'Books', 'Physical and digital books'),
(4, 'Home & Kitchen', 'Home appliances and kitchenware')
ON CONFLICT (id) DO NOTHING;
