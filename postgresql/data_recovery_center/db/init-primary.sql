-- ============================================
-- Data Recovery Center Learning Project
-- Database Schema for Data Center (Primary)
-- ============================================
-- Semua tabel ini akan otomatis direplikasi ke DRC
-- melalui PostgreSQL Streaming Replication (WAL)
-- ============================================

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- Table: application_data
-- Data utama aplikasi (untuk demonstrasi replikasi DC→DRC)
-- ============================================
CREATE TABLE IF NOT EXISTS application_data (
    id              SERIAL PRIMARY KEY,
    uuid            UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    title           VARCHAR(255) NOT NULL,
    content         TEXT,
    category        VARCHAR(100) DEFAULT 'general',
    source_dc       VARCHAR(20) DEFAULT 'dc',
    is_replicated   BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE application_data IS 'Data utama aplikasi - direplikasi dari DC ke DRC via streaming replication';
COMMENT ON COLUMN application_data.source_dc IS 'Sumber data: dc (Data Center) atau drc (Recovery Center)';
COMMENT ON COLUMN application_data.is_replicated IS 'Flag apakah data sudah diverifikasi terreplikasi';

-- ============================================
-- Table: disaster_recovery_logs
-- Log setiap event DR (insert, failover, failback, dll)
-- ============================================
CREATE TABLE IF NOT EXISTS disaster_recovery_logs (
    id              SERIAL PRIMARY KEY,
    event_type      VARCHAR(50) NOT NULL,
    event_source    VARCHAR(20) NOT NULL DEFAULT 'dc',
    description     TEXT,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE disaster_recovery_logs IS 'Log event disaster recovery - mencatat semua aktivitas DR';

-- ============================================
-- Table: failover_history
-- Riwayat failover dan failback
-- ============================================
CREATE TABLE IF NOT EXISTS failover_history (
    id              SERIAL PRIMARY KEY,
    event_type      VARCHAR(20) NOT NULL CHECK (event_type IN ('failover', 'failback')),
    from_host       VARCHAR(255),
    to_host         VARCHAR(255),
    initiated_by    VARCHAR(100),
    duration_ms     INTEGER,
    status          VARCHAR(20) DEFAULT 'completed',
    notes           TEXT,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE failover_history IS 'Riwayat semua proses failover dan failback';

-- ============================================
-- Table: replication_status
-- Tracking status replikasi
-- ============================================
CREATE TABLE IF NOT EXISTS replication_status (
    id              SERIAL PRIMARY KEY,
    check_time      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    primary_host    VARCHAR(255),
    standby_host    VARCHAR(255),
    replication_lag INTERVAL,
    wal_position    VARCHAR(100),
    status          VARCHAR(20) DEFAULT 'active',
    details         JSONB DEFAULT '{}'
);

COMMENT ON TABLE replication_status IS 'Snapshot status replikasi pada waktu tertentu';

-- ============================================
-- Indexes untuk performa query
-- ============================================
CREATE INDEX idx_app_data_category ON application_data(category);
CREATE INDEX idx_app_data_created ON application_data(created_at DESC);
CREATE INDEX idx_app_data_uuid ON application_data(uuid);
CREATE INDEX idx_app_data_source ON application_data(source_dc);
CREATE INDEX idx_dr_logs_type ON disaster_recovery_logs(event_type);
CREATE INDEX idx_dr_logs_created ON disaster_recovery_logs(created_at DESC);
CREATE INDEX idx_failover_type ON failover_history(event_type);
CREATE INDEX idx_failover_created ON failover_history(created_at DESC);

-- ============================================
-- Trigger: Auto-update updated_at
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_app_data_updated
    BEFORE UPDATE ON application_data
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Seed Data
-- Data awal untuk demonstrasi
-- ============================================
INSERT INTO application_data (title, content, category, source_dc) VALUES
    ('Welcome to DRC Learning',
     'Data ini dibuat saat inisialisasi Data Center (Primary). Data akan otomatis direplikasi ke DRC melalui PostgreSQL Streaming Replication.',
     'system', 'dc'),

    ('Memahami Streaming Replication',
     'PostgreSQL Streaming Replication bekerja dengan mengirim Write-Ahead Log (WAL) dari Primary ke Standby secara real-time. Setiap perubahan data di DC akan dikirim ke DRC.',
     'education', 'dc'),

    ('Peran PgBouncer',
     'PgBouncer bertindak sebagai connection pooler antara aplikasi dan PostgreSQL. Dalam arsitektur DC-DRC, PgBouncer membantu mengelola koneksi dan memudahkan switching antara DC dan DRC.',
     'education', 'dc'),

    ('Proses Failover',
     'Failover adalah proses mengalihkan operasi dari DC ke DRC ketika DC mengalami kegagalan. DRC (Standby) dipromosikan menjadi Primary, dan aplikasi diarahkan ke DRC.',
     'education', 'dc'),

    ('Proses Failback',
     'Failback adalah proses mengembalikan operasi dari DRC ke DC setelah DC diperbaiki. DC dikonfigurasi ulang sebagai Primary, dan DRC kembali menjadi Standby.',
     'education', 'dc'),

    ('RPO dan RTO',
     'RPO (Recovery Point Objective) = berapa banyak data yang boleh hilang. RTO (Recovery Time Objective) = berapa lama waktu pemulihan yang bisa ditoleransi. Streaming Replication meminimalkan RPO mendekati nol.',
     'education', 'dc');

-- Log inisialisasi
INSERT INTO disaster_recovery_logs (event_type, event_source, description, metadata) VALUES
    ('SYSTEM_INIT', 'dc',
     'Data Center initialized successfully. Schema created, seed data inserted, ready for replication.',
     '{"tables_created": ["application_data", "disaster_recovery_logs", "failover_history", "replication_status"], "seed_records": 6}');

-- ============================================
-- Informasi
-- ============================================
DO $$
BEGIN
    RAISE NOTICE '============================================';
    RAISE NOTICE '  Database schema created successfully!';
    RAISE NOTICE '  Tables: application_data, disaster_recovery_logs,';
    RAISE NOTICE '          failover_history, replication_status';
    RAISE NOTICE '  Seed data: 6 records inserted';
    RAISE NOTICE '============================================';
END
$$;
