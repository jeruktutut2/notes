-- 000005_add_index_and_constraints.down.sql
-- Rollback: hapus semua index dan constraints yang ditambahkan

-- Hapus constraints
ALTER TABLE orders DROP CONSTRAINT IF EXISTS chk_orders_total_positive;
ALTER TABLE products DROP CONSTRAINT IF EXISTS chk_products_stock_positive;
ALTER TABLE products DROP CONSTRAINT IF EXISTS chk_products_price_positive;

-- Hapus index order_items
DROP INDEX IF EXISTS idx_order_items_product_id;
DROP INDEX IF EXISTS idx_order_items_order_id;

-- Hapus index orders
DROP INDEX IF EXISTS idx_orders_user_status;
DROP INDEX IF EXISTS idx_orders_ordered_at;
DROP INDEX IF EXISTS idx_orders_status;
DROP INDEX IF EXISTS idx_orders_user_id;

-- Hapus index products
DROP INDEX IF EXISTS idx_products_active_stock;
DROP INDEX IF EXISTS idx_products_created_by;
DROP INDEX IF EXISTS idx_products_price;
DROP INDEX IF EXISTS idx_products_name;

-- Hapus index users
DROP INDEX IF EXISTS idx_users_created_at;
DROP INDEX IF EXISTS idx_users_active;
DROP INDEX IF EXISTS idx_users_email;
