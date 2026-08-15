-- 000003_create_products_table.up.sql
-- Membuat tabel products dengan relasi ke users (foreign key)
-- Skenario: CREATE TABLE dengan FOREIGN KEY

CREATE TABLE IF NOT EXISTS products (
    id          BIGSERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    description TEXT,
    price       DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    stock       INTEGER NOT NULL DEFAULT 0,
    sku         VARCHAR(50) NOT NULL UNIQUE,

    -- Foreign key: siapa yang membuat produk ini
    created_by  BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    is_active   BOOLEAN NOT NULL DEFAULT true,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Trigger auto-update updated_at (reuse function dari migration 1)
CREATE TRIGGER set_products_updated_at
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Komentar pada tabel untuk dokumentasi
COMMENT ON TABLE products IS 'Tabel produk dengan relasi ke user sebagai pembuat';
COMMENT ON COLUMN products.sku IS 'Stock Keeping Unit - kode unik produk';
COMMENT ON COLUMN products.price IS 'Harga produk dalam format desimal 12 digit, 2 desimal';
