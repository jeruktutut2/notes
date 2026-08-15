# Dokumentasi Lengkap Arsitektur Data Center (DC) & Disaster Recovery Center (DRC)

Dokumen ini berisi catatan komprehensif, arsitektur, mekanisme kerja, serta contoh konfigurasi nyata untuk penerapan **Main Data Center (DC)** dan **Disaster Recovery Center (DRC)** berbasis PostgreSQL dan infrastruktur High Availability (HA).

---

## 📌 Daftar Isi
1. [Arsitektur & Topologi System](./docs/01-arsitektur-dan-topologi.md)
   - Konsep Dasar DC vs DRC
   - Matriks Target RPO & RTO
   - Diagram Topologi Sistem & Jaringan (Mermaid)
   - Spesifikasi Infrastruktur (Hardware & Networking)
2. [Mekanisme Jaringan, Replikasi & HA](./docs/02-mekanisme-replikasi-dan-jaringan.md)
   - Routing Traffic & GSLB / DNS Failover
   - Sync vs Async Streaming Replication & WAL Archiving
   - Cluster Consensus (Patroni + etcd) & Prevention Split-Brain
3. [Prosedur Pemulihan (Failover, Failback & Reverse SOP)](./docs/03-failover-dan-failback-procedure.md)
   - Skenario Operasional Normal
   - Skenario Disaster & Automatic Switchover ke DRC
   - Mekanisme Reverse (Reverse Replication, Reverse Sync via `pg_rewind`, Reverse Proxy)
   - Skenario Pemulihan (Resynchronization & Failback)
4. [Contoh Konfigurasi Konkret](./config-examples/)
   - PostgreSQL DC Primary (`postgresql-dc-primary.conf`)
   - PostgreSQL DRC Standby (`postgresql-drc-standby.conf`)
   - Cluster Orchestrator Patroni (`patroni-dc.yml` & `patroni-drc.yml`)

---

## 💡 Ringkasan Singkat Elemen Utama

| Komponen | Main Data Center (DC) - Jakarta | Disaster Recovery Center (DRC) - Surabaya |
| :--- | :--- | :--- |
| **Peran** | Primary Active Load (R/W Traffic) | Standby Replica (ReadOnly / Failover Target) |
| **Tier Rating** | Tier 3 (Uptime 99.982%) | Tier 3 / Tier 2+ (Uptime 99.75%+) |
| **Mode Database** | PostgreSQL Leader (Read-Write) | PostgreSQL Standby (Cascade / Streaming Async) |
| **Penyimpanan WAL** | Local NVMe SSD + pgBackRest Archiver | Offsite S3/MinIO Archiver Target |
| **Routing Network** | Primary BGP Route / Primary VIP | Secondary BGP Route / DRC Standby VIP |
| **Estimasi RPO** | **< 1 Detik** (Near Zero Data Loss) | **< 1 Detik** |
| **Estimasi RTO** | **< 30 Detik** (Automated Failover) | **< 30 Detik** |

---

> Referensi lengkap dan pembahasan teknis terinci dapat dibaca pada direktori [`/docs`](./docs/).
