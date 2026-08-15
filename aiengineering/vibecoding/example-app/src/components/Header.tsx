'use client';

import React from 'react';
import { 
  Kanban, 
  FileText, 
  Sparkles, 
  BarChart2, 
  Plus, 
  Search,
  ShieldCheck,
  Zap
} from 'lucide-react';

interface HeaderProps {
  activeTab: 'kanban' | 'prd' | 'ai' | 'metrics';
  setActiveTab: (tab: 'kanban' | 'prd' | 'ai' | 'metrics') => void;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  onOpenCreateModal: () => void;
  taskCount: number;
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  setActiveTab,
  searchQuery,
  setSearchQuery,
  onOpenCreateModal,
  taskCount,
}) => {
  return (
    <header className="sticky top-0 z-30 border-b border-slate-800 bg-slate-950/80 backdrop-blur-md px-4 py-3 md:px-8">
      <div className="mx-auto flex max-w-7xl flex-col gap-4 md:flex-row md:items-center md:justify-between">
        
        {/* Logo & Brand */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 via-purple-500 to-emerald-400 p-0.5 shadow-lg shadow-indigo-500/20">
            <div className="flex h-full w-full items-center justify-center rounded-[10px] bg-slate-950">
              <Zap className="h-5 w-5 text-emerald-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white">VibeFlow</h1>
              <span className="rounded-full bg-emerald-500/10 px-2 py-0.5 text-xs font-semibold text-emerald-400 border border-emerald-500/20">
                v1.0.0 PRD
              </span>
            </div>
            <p className="text-xs text-slate-400">AI-Powered Smart Task & Vibe Coding Companion</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex flex-wrap items-center gap-1 rounded-xl border border-slate-800 bg-slate-900/60 p-1">
          <button
            onClick={() => setActiveTab('kanban')}
            className={`flex items-center gap-2 rounded-lg px-3 py-1.5 text-xs font-medium transition-all ${
              activeTab === 'kanban'
                ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Kanban className="h-4 w-4" />
            <span>Kanban Board</span>
            <span className="ml-1 rounded-full bg-slate-800 px-1.5 py-0.2 text-[10px] font-semibold text-slate-300">
              {taskCount}
            </span>
          </button>

          <button
            onClick={() => setActiveTab('prd')}
            className={`flex items-center gap-2 rounded-lg px-3 py-1.5 text-xs font-medium transition-all ${
              activeTab === 'prd'
                ? 'bg-gradient-to-r from-indigo-600 to-indigo-700 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <FileText className="h-4 w-4" />
            <span>PRD & AGENTS.md</span>
          </button>

          <button
            onClick={() => setActiveTab('ai')}
            className={`flex items-center gap-2 rounded-lg px-3 py-1.5 text-xs font-medium transition-all ${
              activeTab === 'ai'
                ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-md shadow-purple-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <Sparkles className="h-4 w-4 text-pink-400" />
            <span>AI Assistant</span>
          </button>

          <button
            onClick={() => setActiveTab('metrics')}
            className={`flex items-center gap-2 rounded-lg px-3 py-1.5 text-xs font-medium transition-all ${
              activeTab === 'metrics'
                ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-md shadow-emerald-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
            }`}
          >
            <BarChart2 className="h-4 w-4 text-emerald-400" />
            <span>Vibe Metrics</span>
          </button>
        </nav>

        {/* Right Action Controls */}
        <div className="flex items-center gap-2">
          {activeTab === 'kanban' && (
            <>
              <div className="relative flex-1 md:w-48">
                <Search className="absolute left-2.5 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  placeholder="Cari tugas..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full rounded-lg border border-slate-800 bg-slate-900 py-1.5 pl-8 pr-3 text-xs text-slate-200 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
                />
              </div>

              <button
                onClick={onOpenCreateModal}
                className="flex items-center gap-1.5 rounded-lg bg-gradient-to-r from-indigo-500 to-purple-600 px-3 py-1.5 text-xs font-medium text-white shadow-lg shadow-indigo-500/25 transition-all hover:brightness-110 active:scale-95"
              >
                <Plus className="h-4 w-4" />
                <span className="hidden sm:inline">Tambah Tugas</span>
              </button>
            </>
          )}
        </div>

      </div>
    </header>
  );
};
