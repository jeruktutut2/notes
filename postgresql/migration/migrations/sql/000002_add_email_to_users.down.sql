-- 000002_add_email_to_users.down.sql
-- Rollback: hapus kolom email dan phone_number

ALTER TABLE users DROP COLUMN IF EXISTS phone_number;
ALTER TABLE users DROP CONSTRAINT IF EXISTS users_email_unique;
ALTER TABLE users DROP COLUMN IF EXISTS email;
