# Product Requirement Document (PRD): VibeFlow AI Companion

**Nama Produk**: VibeFlow (AI-Powered Smart Task & Project Management)  
**Versi**: 1.0.0  
**Status**: Approved & Ready for Implementation  
**Tanggal**: 26 Juli 2026  
**Penulis**: Vibe Coding Core Team  

---

## 1. Executive Summary & Goals

### 1.1 Problem Statement
Pengembang perangkat lunak modern yang mengadopsi metodologi **Vibe Coding** sering kesulitan menghubungkan antara spesifikasi tertulis (PRD/SDD), manajemen tugas (Kanban), audit keamanan kredensial (`.env`), serta pelacakan performa context window AI secara terpadu dalam satu antarmuka dashboard.

### 1.2 Product Objectives
- Menyediakan platform **Task Management** interaktif yang mengintegrasikan alur kerja Vibe Coding (Planning, TDD, Audit, Refactoring).
- Menyediakan **PRD & Tech Spec Viewer** terintegrasi secara langsung di dalam aplikasi web.
- Menyediakan **AI Vibe Assistant Simulator** untuk melakukan task breakdown otomatis, audit kebocoran rahasia `.env`, dan otomatisasi unit test.
- Menampilkan **Vibe Metrics Dashboard** untuk memantau Test Coverage %, Security Health, Token Context Meter, dan Git Commit Log secara real-time.

---

## 2. Target Users & Personas

1. **Vibe Coder / Fullstack Developer**: Menggunakan AI agent secara intensif, membutuhkan pelacakan tugas berbasis TDD dan status commit.
2. **Product Manager**: Mengutak-atik PRD, memverifikasi kriteria penerimaan (Acceptance Criteria), dan memantau progres fase MVP.
3. **AppSec / Tech Lead**: Memantau skor keamanan aplikasi, larangan hardcoded secrets, serta kebersihan struktur modul.

---

## 3. Key Feature Specifications

### 3.1 Interactive Kanban Board
- **Kolom State**: `To Do`, `In Progress`, `Review`, `Done`.
- **Atribut Tugas**: ID (`TASK-101`), Judul, Deskripsi, Prioritas (`High`, `Medium`, `Low`), Category Tag (`Feature`, `Bugfix`, `TDD`, `Security`, `Refactor`), Status Test (`Passing`, `Failing`, `Pending`), dan Security Audit Badge.
- **Interaksi**: Drag-and-drop / tombol percepatan status, pencarian real-time, filter tag.

### 3.2 Integrated PRD & Architecture Viewer
- Modal/Tab dedicated untuk membaca dokumen PRD resmi ini (`PRD.md`) dan Dokumen Standar Preferensi Kode (`AGENTS.md`).
- Mendukung sintaks Markdown yang diformat dengan baik.

### 3.3 AI Vibe Assistant Simulator
- Input box untuk mengetik prompt instruksi AI (atau memilih contoh prompt sekali klik).
- **Aksi Otomatis**:
  - *Breakdown Feature*: Mengurai 1 fitur besar menjadi 3 sub-tugas di Kanban.
  - *Security Audit*: Memindai codebase lokal untuk mendeteksi kredensial rahasia yang ter-hardcode dan menandai alert.
  - *TDD Test Generator*: Membuat test suite Vitest/Jest otomatis untuk tugas yang sedang dikerjakan.

### 3.4 Vibe Coding Metrics Dashboard
- **Test Coverage Meter**: Visualisasi % cakupan pengujian (Target > 85%).
- **Security Health Score**: Skor keamanan 0-100% berdasarkan audit kredensial & sanitasi data.
- **Token Context Meter**: Indikator kapasitas context window yang terpakai (Alert saat > 80% untuk mengingatkan reset chat).
- **Git Activity Log**: Stream riwayat commit lokal simulasi.

---

## 4. Technical Architecture & Stack

- **Framework**: Next.js 15+ (App Router, TypeScript)
- **Styling**: Tailwind CSS v4 (Glassmorphism, Dark Mode Slate Palette)
- **Icons**: Lucide React
- **State & Storage**: React Local State + LocalStorage Persistence
- **Deployment target**: Vercel / Node.js Standalone

---

## 5. Acceptance Criteria (Criteria Penerimaan)

- [x] Aplikasi berjalan tanpa error di port `localhost:3000` dengan Next.js dev server.
- [x] Pengguna dapat menambah, mengedit, memindahkan status, dan menghapus tugas di Kanban Board.
- [x] Tombol simulasi AI (Breakdown, Security Audit, Test Generation) memunculkan feedback visual dan memperbarui data board & dashboard.
- [x] Dokumen PRD dan AGENTS.md dapat dibaca melalui tab PRD Viewer.
- [x] Perubahan data bertahan di LocalStorage saat browser direfresh.
