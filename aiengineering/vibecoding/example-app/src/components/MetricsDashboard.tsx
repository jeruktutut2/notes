'use client';

import React from 'react';
import { VibeMetrics, GitCommitLog } from '@/types/vibe';
import { ShieldCheck, CheckCircle, Cpu, GitCommit, ArrowUpRight } from 'lucide-react';

interface MetricsDashboardProps {
  metrics: VibeMetrics;
  commits: GitCommitLog[];
}

export const MetricsDashboard: React.FC<MetricsDashboardProps> = ({ metrics, commits }) => {
  return (
    <div className="mx-auto max-w-5xl flex flex-col gap-6">
      
      {/* 4 Cards Grid */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        
        {/* Test Coverage */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur-sm shadow-xl">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-400">Test Coverage</span>
            <div className="rounded-lg bg-emerald-500/10 p-2 text-emerald-400">
              <CheckCircle className="h-4 w-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white mb-1">{metrics.testCoverage}%</div>
          <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
            <div
              className="bg-emerald-500 h-2 rounded-full transition-all duration-500"
              style={{ width: `${metrics.testCoverage}%` }}
            ></div>
          </div>
          <p className="mt-2 text-[11px] text-slate-400">Target Vibe TDD: &gt; 85%</p>
        </div>

        {/* Security Health */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur-sm shadow-xl">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-400">Security Score</span>
            <div className="rounded-lg bg-indigo-500/10 p-2 text-indigo-400">
              <ShieldCheck className="h-4 w-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white mb-1">{metrics.securityScore}/100</div>
          <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
            <div
              className="bg-indigo-500 h-2 rounded-full transition-all duration-500"
              style={{ width: `${metrics.securityScore}%` }}
            ></div>
          </div>
          <p className="mt-2 text-[11px] text-slate-400">Status: Kredensial .env Aman</p>
        </div>

        {/* Context Token Usage */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur-sm shadow-xl">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-400">Context Window Token</span>
            <div className="rounded-lg bg-purple-500/10 p-2 text-purple-400">
              <Cpu className="h-4 w-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white mb-1">{metrics.contextTokenUsage}%</div>
          <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
            <div
              className={`h-2 rounded-full transition-all duration-500 ${
                metrics.contextTokenUsage > 75 ? 'bg-rose-500' : 'bg-purple-500'
              }`}
              style={{ width: `${metrics.contextTokenUsage}%` }}
            ></div>
          </div>
          <p className="mt-2 text-[11px] text-slate-400">
            {metrics.contextTokenUsage > 75 ? 'Saran: Lakukan Reset Chat!' : 'Context Sehat & Responsif'}
          </p>
        </div>

        {/* Git Commits Count */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur-sm shadow-xl">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-slate-400">Git Commit Count</span>
            <div className="rounded-lg bg-pink-500/10 p-2 text-pink-400">
              <GitCommit className="h-4 w-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-white mb-1">{metrics.commitCount} Commits</div>
          <p className="text-[11px] text-emerald-400 flex items-center gap-1 mt-3">
            <ArrowUpRight className="h-3.5 w-3.5" />
            Frequent Commit Active
          </p>
        </div>

      </div>

      {/* Live Git Commit Stream */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6 backdrop-blur-sm shadow-xl">
        <h3 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
          <GitCommit className="h-4 w-4 text-indigo-400" />
          <span>Simulasi Stream Git Commit History</span>
        </h3>

        <div className="flex flex-col gap-3">
          {commits.map((c) => (
            <div
              key={c.id}
              className="flex flex-col gap-1 rounded-xl border border-slate-800/80 bg-slate-950 p-3 sm:flex-row sm:items-center sm:justify-between"
            >
              <div className="flex items-center gap-3">
                <span className="font-mono text-xs font-semibold text-indigo-400 bg-indigo-500/10 px-2 py-0.5 rounded border border-indigo-500/20">
                  {c.hash}
                </span>
                <span className="text-xs text-slate-200">{c.message}</span>
              </div>
              <span className="text-[11px] text-slate-400">{c.timestamp}</span>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};
