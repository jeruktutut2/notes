-- 000002_add_email_to_users.up.sql
-- Menambahkan kolom email ke tabel users
-- Skenario: ALTER TABLE - menambah kolom baru dengan constraint

ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(255);

-- Tambahkan unique constraint pada email
-- Menggunakan nama constraint eksplisit agar mudah di-rollback
ALTER TABLE users ADD CONSTRAINT users_email_unique UNIQUE (email);

-- Tambahkan kolom phone_number (opsional, bisa NULL)
ALTER TABLE users ADD COLUMN IF NOT EXISTS phone_number VARCHAR(20);
