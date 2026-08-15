-- 000004_create_orders_table.down.sql
-- Rollback: hapus tabel orders, order_items, dan enum

DROP TRIGGER IF EXISTS set_orders_updated_at ON orders;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TYPE IF EXISTS order_status;
