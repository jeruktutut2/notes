-- 000004_create_orders_table.up.sql
-- Membuat tabel orders dan order_items
-- Skenario: multiple tables dalam satu migration + junction table

-- Enum untuk status order
CREATE TYPE order_status AS ENUM ('pending', 'processing', 'shipped', 'delivered', 'cancelled');

-- Tabel orders (header)
CREATE TABLE IF NOT EXISTS orders (
    id              BIGSERIAL PRIMARY KEY,
    order_number    VARCHAR(50) NOT NULL UNIQUE,
    user_id         BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status          order_status NOT NULL DEFAULT 'pending',
    total_amount    DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    notes           TEXT,
    ordered_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Tabel order_items (detail/junction)
CREATE TABLE IF NOT EXISTS order_items (
    id          BIGSERIAL PRIMARY KEY,
    order_id    BIGINT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id  BIGINT NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity    INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unit_price  DECIMAL(12, 2) NOT NULL,
    subtotal    DECIMAL(15, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Trigger auto-update updated_at
CREATE TRIGGER set_orders_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE orders IS 'Tabel order header';
COMMENT ON TABLE order_items IS 'Tabel order detail (junction antara orders dan products)';
COMMENT ON COLUMN order_items.subtotal IS 'Kolom generated: quantity * unit_price';
