CREATE DATABASE IF NOT EXISTS company_db;
USE company_db;

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Buat User Root Remote
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'rootpassword';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;

-- Buat User Replikasi MySQL GTID
CREATE USER IF NOT EXISTS 'repl_user'@'%' IDENTIFIED WITH mysql_native_password BY 'repl_password';
GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'repl_user'@'%';

-- Buat User Orchestrator Monitoring & Topology Management
CREATE USER IF NOT EXISTS 'orc_client'@'%' IDENTIFIED WITH mysql_native_password BY 'orc_password';
GRANT REPLICATION SLAVE, REPLICATION CLIENT, SUPER, PROCESS, SELECT ON *.* TO 'orc_client'@'%';

FLUSH PRIVILEGES;

-- Seed Data Awal
INSERT INTO employees (name, position) VALUES ('Alice Primary', 'System Architect');
INSERT INTO employees (name, position) VALUES ('Bob Admin', 'Database Administrator');
