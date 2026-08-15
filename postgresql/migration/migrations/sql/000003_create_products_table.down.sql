-- 000003_create_products_table.down.sql
-- Rollback: hapus tabel products

DROP TRIGGER IF EXISTS set_products_updated_at ON products;
DROP TABLE IF EXISTS products;
