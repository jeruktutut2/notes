-- ============================================================================
-- SKENARIO PROGRESIF - STAGE 2: SHARDING & DISTRIBUTED TABLES (CITUS)
-- ============================================================================

-- 1. Pendaftaran Worker Nodes ke Coordinator Cluster (jika belum terdaftar)
SELECT citus_add_node('citus-worker-1', 5432) 
WHERE NOT EXISTS (SELECT 1 FROM citus_get_active_worker_nodes() WHERE node_name = 'citus-worker-1');

SELECT citus_add_node('citus-worker-2', 5432) 
WHERE NOT EXISTS (SELECT 1 FROM citus_get_active_worker_nodes() WHERE node_name = 'citus-worker-2');

-- 2. DDL Pembuatan Schema Tabel
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS categories CASCADE;

-- Tabel Users (Akan dishard berdasarkan user_id)
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    country_code VARCHAR(5) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabel Orders (Akan dishard & co-located dengan users berdasarkan user_id)
CREATE TABLE orders (
    order_id BIGSERIAL,
    user_id BIGINT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(12, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    PRIMARY KEY (user_id, order_id)
);

-- Tabel Categories (Reference Table - direplikasi utuh ke semua worker node)
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    description TEXT
);

-- 3. Konversi Tabel menjadi Distributed Tables & Reference Table di Citus Cluster
SELECT create_distributed_table('users', 'user_id');
SELECT create_distributed_table('orders', 'user_id');
SELECT create_reference_table('categories');

-- 4. Pengisian Data Sampel (Seeding Data)
INSERT INTO categories (category_name, description) VALUES
('Electronics', 'Gadgets and electronic items'),
('Clothing', 'Apparel and footwear'),
('Books', 'Physical and electronic books'),
('Home & Kitchen', 'Furniture and home accessories');

-- Generasi 10,000 data pengguna secara acak
INSERT INTO users (name, email, country_code, created_at)
SELECT 
    'User_' || i,
    'user_' || i || '@example.com',
    (ARRAY['ID', 'SG', 'MY', 'US', 'JP'])[floor(random() * 5 + 1)],
    NOW() - (random() * interval '365 days')
FROM generate_series(1, 10000) s(i);

-- Generasi 20,000 data pesanan
INSERT INTO orders (user_id, total_amount, status, order_date)
SELECT 
    floor(random() * 10000 + 1)::BIGINT,
    (random() * 500 + 10)::NUMERIC(12,2),
    (ARRAY['COMPLETED', 'PENDING', 'CANCELLED', 'SHIPPED'])[floor(random() * 4 + 1)],
    NOW() - (random() * interval '180 days')
FROM generate_series(1, 20000) s(i);
