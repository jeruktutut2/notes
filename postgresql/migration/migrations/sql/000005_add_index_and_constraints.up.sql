-- 000005_add_index_and_constraints.up.sql
-- Menambahkan index dan constraints untuk optimasi performa
-- Skenario: ALTER TABLE, CREATE INDEX, partial index

-- ==========================================
-- INDEX pada tabel users
-- ==========================================

-- Index pada email untuk pencarian cepat
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Index pada is_active untuk filter user aktif
CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active) WHERE is_active = true;

-- Index pada created_at untuk sorting
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at DESC);

-- ==========================================
-- INDEX pada tabel products
-- ==========================================

-- Index pada nama produk untuk pencarian (case-insensitive)
CREATE INDEX IF NOT EXISTS idx_products_name ON products USING gin(to_tsvector('simple', name));

-- Index pada price untuk range query
CREATE INDEX IF NOT EXISTS idx_products_price ON products(price);

-- Index pada created_by untuk join dengan users
CREATE INDEX IF NOT EXISTS idx_products_created_by ON products(created_by);

-- Partial index: hanya produk aktif yang memiliki stok
CREATE INDEX IF NOT EXISTS idx_products_active_stock ON products(stock)
    WHERE is_active = true AND stock > 0;

-- ==========================================
-- INDEX pada tabel orders
-- ==========================================

-- Index pada user_id untuk query order per user
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);

-- Index pada status untuk filter
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

-- Index pada ordered_at untuk range query tanggal
CREATE INDEX IF NOT EXISTS idx_orders_ordered_at ON orders(ordered_at DESC);

-- Composite index: user + status (query paling umum)
CREATE INDEX IF NOT EXISTS idx_orders_user_status ON orders(user_id, status);

-- ==========================================
-- INDEX pada tabel order_items
-- ==========================================

-- Index pada order_id dan product_id
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);

-- ==========================================
-- CONSTRAINT tambahan
-- ==========================================

-- Pastikan harga produk tidak negatif
ALTER TABLE products ADD CONSTRAINT chk_products_price_positive CHECK (price >= 0);

-- Pastikan stok tidak negatif
ALTER TABLE products ADD CONSTRAINT chk_products_stock_positive CHECK (stock >= 0);

-- Pastikan total_amount order tidak negatif
ALTER TABLE orders ADD CONSTRAINT chk_orders_total_positive CHECK (total_amount >= 0);
