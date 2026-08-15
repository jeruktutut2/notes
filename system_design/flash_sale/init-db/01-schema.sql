-- Flash Sale System Schema

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Products Table
CREATE TABLE IF NOT EXISTS products (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL,
    original_price  DECIMAL(15,2) NOT NULL,
    description     TEXT,
    category        VARCHAR(100),
    image_url       TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Flash Sale Events Table
CREATE TABLE IF NOT EXISTS flash_sales (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id      UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    sale_price      DECIMAL(15,2) NOT NULL,
    original_stock  INTEGER NOT NULL CHECK (original_stock > 0),
    remaining_stock INTEGER NOT NULL CHECK (remaining_stock >= 0),
    max_per_user    INTEGER NOT NULL DEFAULT 1,
    start_time      TIMESTAMPTZ NOT NULL,
    end_time        TIMESTAMPTZ NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'DRAFT'
                    CHECK (status IN ('DRAFT','UPCOMING','ACTIVE',
                                      'SOLD_OUT','ENDED','CANCELLED')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_flash_sales_status ON flash_sales(status);
CREATE INDEX IF NOT EXISTS idx_flash_sales_start_time ON flash_sales(start_time);

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           VARCHAR(255) UNIQUE NOT NULL,
    name            VARCHAR(255) NOT NULL,
    phone           VARCHAR(50),
    password_hash   VARCHAR(255) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id           UUID NOT NULL REFERENCES users(id),
    flash_sale_id     UUID NOT NULL REFERENCES flash_sales(id),
    product_id        UUID NOT NULL REFERENCES products(id),
    price             DECIMAL(15,2) NOT NULL,
    status            VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                      CHECK (status IN ('PENDING','AWAITING_PAYMENT',
                                        'PAID','EXPIRED','CANCELLED',
                                        'REFUNDED','PAYMENT_FAILED')),
    idempotency_key   VARCHAR(255) NOT NULL UNIQUE,
    payment_deadline  TIMESTAMPTZ,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_orders_user_sale ON orders(user_id, flash_sale_id);
CREATE INDEX IF NOT EXISTS idx_orders_status_deadline ON orders(status, payment_deadline);
CREATE INDEX IF NOT EXISTS idx_orders_idempotency ON orders(idempotency_key);

-- Payments Table
CREATE TABLE IF NOT EXISTS payments (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id        UUID NOT NULL REFERENCES orders(id),
    amount          DECIMAL(15,2) NOT NULL,
    payment_method  VARCHAR(50),
    gateway_ref_id  VARCHAR(255),
    status          VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                    CHECK (status IN ('PENDING','PROCESSING',
                                      'SUCCESS','FAILED','REFUNDED')),
    paid_at         TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_payments_order ON payments(order_id);
CREATE INDEX IF NOT EXISTS idx_payments_gateway_ref ON payments(gateway_ref_id);

-- Insert Sample Product & Flash Sale for Initial Setup
INSERT INTO products (id, name, original_price, description, category, image_url)
VALUES (
    '11111111-1111-1111-1111-111111111111',
    'iPhone 16 Pro Max 256GB',
    20000000.00,
    'Flash Sale Special iPhone 16 Pro Max',
    'Electronics',
    'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO users (id, email, name, phone, password_hash)
VALUES (
    '22222222-2222-2222-2222-222222222222',
    'user1@example.com',
    'Budi Santoso',
    '08123456789',
    'hashed_password_123'
), (
    '33333333-3333-3333-3333-333333333333',
    'user2@example.com',
    'Siti Rahma',
    '08987654321',
    'hashed_password_456'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO flash_sales (id, product_id, sale_price, original_stock, remaining_stock, max_per_user, start_time, end_time, status)
VALUES (
    '44444444-4444-4444-4444-444444444444',
    '11111111-1111-1111-1111-111111111111',
    5000000.00,
    5,
    5,
    1,
    NOW(),
    NOW() + INTERVAL '2 hours',
    'ACTIVE'
) ON CONFLICT (id) DO NOTHING;
