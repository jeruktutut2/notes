# 01. Arsitektur & Topologi Data Center (DC) & Disaster Recovery Center (DRC)

## 1. Konsep Dasar DC vs DRC

### Main Data Center (DC)
Main Data Center adalah fasilitas fisik terpusat yang menampung infrastruktur komputasi utama (server, storage, networking switch, router, firewall) serta melayani 100% *traffic operational* harian dari pengguna akhir (Users/Clients). DC dirancang memiliki keandalan tinggi (minimal Tier 3) dengan komponen *redundant* (N+1 atau 2N) pada sistem daya (UPS, Generator) dan pendingin (CRAC/HVAC).

### Disaster Recovery Center (DRC)
Disaster Recovery Center adalah fasilitas infrastruktur sekunder yang terletak di lokasi geografis terpisah dari DC utama. DRC berfungsi sebagai lokasi pengganti (*failover site*) yang siap mengambil alih seluruh fungsi layanan kritis (*business continuity*) apabila DC utama mengalami pemadaman total (*catastrophic failure*) akibat bencana alam, kegagalan daya masif, serangan siber, atau kerusakan fisik infrastruktur.

---

## 2. Prinsip Pemisahan Geografis & Klasifikasi Tier

1. **Jarak Geografis (Geographic Separation)**:
   - Jarak minimum antara DC (misal: Jakarta) dan DRC (misal: Surabaya / Bali) idealnya **> 100 km - 500 km**.
   - **Tujuan**: Memastikan bencana alam lokal (gempa bumi, banjir bandang, pemadaman listrik regional) tidak memengaruhi kedua lokasi secara bersamaan.
   - **Tantangan**: Semakin jauh jarak, semakin besar *network latency* (latensi RTT ~10-15 ms). Hal ini menentukan penggunaan replikasi **Asynchronous** untuk menjaga performa aplikasi di DC Utama.

2. **Jaringan Listrik & Fiber Optik Terpisah (Independent Power Grid & Routing)**:
   - DC dan DRC harus terhubung ke *substation* listrik (PLN) yang berbeda dan dilewati jalur kabel *Fiber Optik* dengan *path diversity* (jalur fisik kabel tidak berada di parit/pipa yang sama).

---

## 3. Matriks Target RPO & RTO

| Parameter | Definisi | Target Ideal | Solusi Teknis |
| :--- | :--- | :--- | :--- |
| **RPO** (*Recovery Point Objective*) | Batas toleransi maksimum kehilangan data yang diukur dalam satuan waktu sebelum insiden terjadi. | **< 1 Detik** (Near Zero) | Physical Streaming Replication (PostgreSQL / WAL Archiving via pgBackRest ke Object Storage). |
| **RTO** (*Recovery Time Objective*) | Durasi waktu maksimum yang dibutuhkan untuk memulihkan seluruh sistem dari saat kegagalan hingga sistem siap melayani user kembali. | **< 30 Detik - 2 Menit** | Automatic Distributed Consensus Cluster Orchestration (**Patroni + etcd**) & GSLB / DNS Switchover. |

---

## 4. Diagram Topologi Sistem (Mermaid)

```mermaid
flowchart TB
    subgraph CLIENTS ["🌐 External Clients / End-Users"]
        Users["User Applications / Web Browsers"]
    end

    subgraph TRAFFIC_LAYER ["🔀 Traffic Routing & Global Load Balancing"]
        GSLB["GSLB / DNS Failover\n(Cloudflare / Route53 / BGP Anycast)"]
    end

    subgraph DC_SITE ["🏢 MAIN DATA CENTER (DC) - JAKARTA (Active Site)"]
        direction TB
        subgraph DC_NET ["Network & Security Layer"]
            DC_FW["Firewall / Edge Router"]
            DC_LB["HAProxy / VIP (192.168.10.100)"]
        end
        
        subgraph DC_APP ["Application Tier"]
            DC_App1["App Server 01"]
            DC_App2["App Server 02"]
        end
        
        subgraph DC_DB ["Database Tier (PostgreSQL Primary Cluster)"]
            DC_DB_Leader["PostgreSQL Node 1\n(LEADER / Read-Write)\nIP: 192.168.10.11"]
            DC_DB_Replica["PostgreSQL Node 2\n(Sync Replica)\nIP: 192.168.10.12"]
            DC_Etcd["etcd Consensus Cluster\n(DC Nodes)"]
        end
    end

    subgraph INTERCONNECT ["⚡ Inter-Site High Speed Connectivity"]
        DarkFiber["Dedicated Dark Fiber / IPSec VPN Tunnel\n(Latency: ~12ms, Bandwidth: 10 Gbps)"]
    end

    subgraph DRC_SITE ["🏬 DISASTER RECOVERY CENTER (DRC) - SURABAYA (Standby Site)"]
        direction TB
        subgraph DRC_NET ["Network & Security Layer"]
            DRC_FW["Firewall / Edge Router"]
            DRC_LB["HAProxy / VIP (192.168.20.100)"]
        end
        
        subgraph DRC_APP ["Application Tier (Warm Standby)"]
            DRC_App1["App Server DRC 01"]
            DRC_App2["App Server DRC 02"]
        end
        
        subgraph DRC_DB ["Database Tier (PostgreSQL Standby Cluster)"]
            DRC_DB_Standby["PostgreSQL Node 3\n(STANDBY / Async Replica)\nIP: 192.168.20.11"]
            DRC_Etcd["etcd Consensus Cluster\n(DRC Node)"]
        end
    end

    %% Flow Connections
    Users --> GSLB
    GSLB -- "Primary Traffic (Normal)" --> DC_FW
    GSLB -. "Failover Traffic (Disaster)" .-> DRC_FW

    DC_FW --> DC_LB
    DC_LB --> DC_App1 & DC_App2
    DC_App1 & DC_App2 --> DC_DB_Leader

    %% Intra-DC Sync Replication
    DC_DB_Leader == "Sync Replication (LAN < 1ms)" ==> DC_DB_Replica

    %% Inter-DC Async Streaming Replication
    DC_DB_Leader == "Async Physical Streaming Replication via Tunnel" ==> DarkFiber
    DarkFiber ==> DRC_DB_Standby

    DRC_FW --> DRC_LB
    DRC_LB --> DRC_App1 & DRC_App2
    DRC_App1 & DRC_App2 -. "ReadOnly / Prepared for Leader" .-> DRC_DB_Standby

    DC_Etcd <--- "Distributed Consensus" ---> DarkFiber <--- "Distributed Consensus" ---> DRC_Etcd
```

---

## 5. Rincian Komponen Infrastruktur

### A. Compute & Server Tier
- **DC (Main)**: Minimum 2-3 Node Server fisik/VM untuk Application & Database Cluster.
- **DRC (Standby)**: Minimum 1-2 Node Server fisik/VM dengan spesifikasi CPU/RAM setara (*1:1 Sizing*) agar mampu menampung 100% beban puncak saat failover terjadi.

### B. Network & Security Tier
- **Dual ISP Provider**: BGP Peering multihomed di kedua lokasi.
- **L2/L3 Interconnect**: VXLAN / EVPN over IPSec VPN untuk komunikasi IP privat antar datacenter.
- **Health-check Probes**: Pengujian otomatis setiap 5 detik dari luar jaringan (*External Heartbeat Runner*) untuk mendeteksi *unreachability*.
