import { Task, VibeMetrics, GitCommitLog } from '@/types/vibe';

export const INITIAL_TASKS: Task[] = [
  {
    id: 'TASK-101',
    title: 'Implement Spec-Driven Development (SDD) Schema',
    description: 'Create spec.md for auth endpoint and define payload interfaces before coding.',
    status: 'done',
    priority: 'high',
    category: 'feature',
    testStatus: 'passing',
    hasSecurityAudit: true,
    createdAt: '2026-07-26 10:00',
  },
  {
    id: 'TASK-102',
    title: 'Audit .env Secrets & Prevent Hardcoding',
    description: 'Ensure API keys are loaded via process.env and .env is present in .gitignore.',
    status: 'done',
    priority: 'high',
    category: 'security',
    testStatus: 'passing',
    hasSecurityAudit: true,
    createdAt: '2026-07-26 10:30',
  },
  {
    id: 'TASK-103',
    title: 'Write Unit Tests for Payment Processor (TDD)',
    description: 'Write Vitest suite with edge cases before implementing refund calculation logic.',
    status: 'in_progress',
    priority: 'medium',
    category: 'tdd',
    testStatus: 'failing',
    hasSecurityAudit: false,
    createdAt: '2026-07-26 11:15',
  },
  {
    id: 'TASK-104',
    title: 'Refactor Monolithic Component (350+ lines)',
    description: 'Extract Header, Sidebar, and Chart components into separate modular files.',
    status: 'todo',
    priority: 'medium',
    category: 'refactor',
    testStatus: 'pending',
    hasSecurityAudit: false,
    createdAt: '2026-07-26 12:00',
  },
  {
    id: 'TASK-105',
    title: 'Fix CORS Preflight Error on Staging',
    description: 'Add defensive headers and verify OPTIONS preflight response in Express backend.',
    status: 'review',
    priority: 'high',
    category: 'bugfix',
    testStatus: 'passing',
    hasSecurityAudit: true,
    createdAt: '2026-07-26 13:20',
  },
];

export const INITIAL_METRICS: VibeMetrics = {
  testCoverage: 88,
  securityScore: 95,
  contextTokenUsage: 42,
  commitCount: 14,
};

export const INITIAL_COMMITS: GitCommitLog[] = [
  {
    id: '1',
    hash: 'a9f12b8',
    message: 'feat(auth): add SDD specification document for OAuth2 flow',
    timestamp: '10 mins ago',
    type: 'feat',
  },
  {
    id: '2',
    hash: '7c810de',
    message: 'sec(audit): sanitize user inputs and remove hardcoded API key',
    timestamp: '25 mins ago',
    type: 'sec',
  },
  {
    id: '3',
    hash: '3e491ab',
    message: 'test(payment): add Vitest breaking test suite for currency conversion',
    timestamp: '45 mins ago',
    type: 'test',
  },
  {
    id: '4',
    hash: '8f001c2',
    message: 'refactor(ui): extract modular components to keep files < 150 lines',
    timestamp: '1 hour ago',
    type: 'refactor',
  },
];

export const PRD_CONTENT = `# Product Requirement Document (PRD): VibeFlow AI Companion

**Nama Produk**: VibeFlow (AI-Powered Smart Task & Project Management)  
**Versi**: 1.0.0  
**Status**: Approved & Ready for Implementation  
**Tanggal**: 26 Juli 2026  

---

## 1. Executive Summary & Goals

### 1.1 Problem Statement
Pengembang perangkat lunak modern yang mengadopsi metodologi **Vibe Coding** sering kesulitan menghubungkan antara spesifikasi tertulis (PRD/SDD), manajemen tugas (Kanban), audit keamanan kredensial (\`.env\`), serta pelacakan performa context window AI secara terpadu dalam satu antarmuka dashboard.

### 1.2 Product Objectives
- Menyediakan platform **Task Management** interaktif yang mengintegrasikan alur kerja Vibe Coding (Planning, TDD, Audit, Refactoring).
- Menyediakan **PRD & Tech Spec Viewer** terintegrasi secara langsung di dalam aplikasi web.
- Menyediakan **AI Vibe Assistant Simulator** untuk melakukan task breakdown otomatis, audit kebocoran rahasia \`.env\`, dan otomatisasi unit test.
- Menampilkan **Vibe Metrics Dashboard** untuk memantau Test Coverage %, Security Health, Token Context Meter, dan Git Commit Log secara real-time.

---

## 2. Target Users & Personas

1. **Vibe Coder / Fullstack Developer**: Menggunakan AI agent secara intensif, membutuhkan pelacakan tugas berbasis TDD dan status commit.
2. **Product Manager**: Mengutak-atik PRD, memverifikasi kriteria penerimaan (Acceptance Criteria), dan memantau progres fase MVP.
3. **AppSec / Tech Lead**: Memantau skor keamanan aplikasi, larangan hardcoded secrets, serta kebersihan struktur modul.

---

## 3. Key Feature Specifications

### 3.1 Interactive Kanban Board
- **Kolom State**: \`To Do\`, \`In Progress\`, \`Review\`, \`Done\`.
- **Atribut Tugas**: ID (\`TASK-101\`), Judul, Deskripsi, Prioritas (\`High\`, \`Medium\`, \`Low\`), Category Tag (\`Feature\`, \`Bugfix\`, \`TDD\`, \`Security\`, \`Refactor\`), Status Test (\`Passing\`, \`Failing\`, \`Pending\`), dan Security Audit Badge.
- **Interaksi**: Drag-and-drop / tombol percepatan status, pencarian real-time, filter tag.

### 3.2 Integrated PRD & Architecture Viewer
- Modal/Tab dedicated untuk membaca dokumen PRD resmi ini (\`PRD.md\`) dan Dokumen Standar Preferensi Kode (\`AGENTS.md\`).

### 3.3 AI Vibe Assistant Simulator
- Input box untuk mengetik prompt instruksi AI (atau memilih contoh prompt sekali klik).
- **Aksi Otomatis**:
  - *Breakdown Feature*: Mengurai 1 fitur besar menjadi 3 sub-tugas di Kanban.
  - *Security Audit*: Memindai codebase lokal untuk mendeteksi kredensial rahasia yang ter-hardcode dan menandai alert.
  - *TDD Test Generator*: Membuat test suite Vitest/Jest otomatis untuk tugas yang sedang dikerjakan.

---

## 4. Technical Architecture & Stack

- **Framework**: Next.js 15+ (App Router, TypeScript)
- **Styling**: Tailwind CSS v4 (Glassmorphism, Dark Mode Slate Palette)
- **Icons**: Lucide React
- **State & Storage**: React Local State + LocalStorage Persistence
`;

export const AGENTS_CONTENT = `# Coding Preferences & Agent Instructions (AGENTS.md)

File ini mendefinisikan aturan dan konvensi pengkodean yang WAJIB dipatuhi oleh seluruh AI Coding Assistants saat memodifikasi aplikasi **VibeFlow**.

## 1. Core Stack Rules
- **Framework**: Next.js (App Router, React 19 / Client Components dengan \`'use client'\` jika memerlukan state interactivity).
- **Language**: TypeScript Strict Mode. Dilarang keras menggunakan tipe \`any\`.
- **Styling**: Tailwind CSS. Gunakan kelas utility Tailwind murni dengan palet warna dark mode (\`bg-slate-950\`, \`bg-slate-900/80\`, \`border-slate-800\`, \`text-slate-100\`, \`emerald-500\`, \`indigo-500\`).
- **Icons**: \`lucide-react\`.

## 2. Component Architecture
- Semua komponen disimpan di folder \`@/src/components/\`.
- Pisahkan UI Komponen menjadi file-file kecil yang modular (< 150 baris per file):
  - \`@/src/components/Header.tsx\`
  - \`@/src/components/KanbanBoard.tsx\`
  - \`@/src/components/TaskCard.tsx\`
  - \`@/src/components/PrdViewer.tsx\`
  - \`@/src/components/AiSimulator.tsx\`
  - \`@/src/components/MetricsDashboard.tsx\`
  - \`@/src/components/TaskModal.tsx\`
`;
