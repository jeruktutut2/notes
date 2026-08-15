-- Migration: Create notifications table
-- Notification Service database schema

CREATE TABLE IF NOT EXISTS notifications (
    id VARCHAR(36) PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL,
    type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'SENT',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Type values: ORDER_COMPLETED, ORDER_FAILED
-- Status values: SENT, FAILED

CREATE INDEX idx_notifications_order_id ON notifications(order_id);
CREATE INDEX idx_notifications_type ON notifications(type);
