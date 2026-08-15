'use client';

import React, { useState } from 'react';
import { Task, VibeMetrics, GitCommitLog } from '@/types/vibe';
import { Sparkles, ShieldCheck, Terminal, Play, RefreshCw, CheckCircle2 } from 'lucide-react';

interface AiSimulatorProps {
  tasks: Task[];
  setTasks: React.Dispatch<React.SetStateAction<Task[]>>;
  metrics: VibeMetrics;
  setMetrics: React.Dispatch<React.SetStateAction<VibeMetrics>>;
  setCommits: React.Dispatch<React.SetStateAction<GitCommitLog[]>>;
}

export const AiSimulator: React.FC<AiSimulatorProps> = ({
  tasks,
  setTasks,
  metrics,
  setMetrics,
  setCommits,
}) => {
  const [promptInput, setPromptInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [logs, setLogs] = useState<string[]>([
    'Vibe AI Subagent v2.4 initialized.',
    'System ready. Select a preset prompt or type a custom task directive.',
  ]);

  const addLog = (msg: string) => {
    setLogs((prev) => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);
  };

  const handleBreakdownFeature = () => {
    setIsProcessing(true);
    addLog('Executing: Feature Breakdown based on PRD specs...');

    setTimeout(() => {
      const newSubtasks: Task[] = [
        {
          id: `TASK-${Math.floor(100 + Math.random() * 900)}`,
          title: 'Design DB Schema for User Preferences',
          description: 'Created Prisma schema migration for user settings as defined in spec.md.',
          status: 'todo',
          priority: 'high',
          category: 'feature',
          testStatus: 'pending',
          hasSecurityAudit: false,
          createdAt: new Date().toISOString().slice(0, 16).replace('T', ' '),
        },
        {
          id: `TASK-${Math.floor(100 + Math.random() * 900)}`,
          title: 'Implement API Endpoint GET /api/user/prefs',
          description: 'Constructed Next.js Route Handler with Zod schema validation.',
          status: 'todo',
          priority: 'medium',
          category: 'feature',
          testStatus: 'pending',
          hasSecurityAudit: false,
          createdAt: new Date().toISOString().slice(0, 16).replace('T', ' '),
        },
      ];

      setTasks((prev) => [...newSubtasks, ...prev]);
      addLog('Success: Added 2 decomposed sub-tasks to To-Do Kanban column.');
      setIsProcessing(false);
    }, 1000);
  };

  const handleSecurityAudit = () => {
    setIsProcessing(true);
    addLog('Executing: Automated OWASP & .env Credentials Security Audit...');

    setTimeout(() => {
      setTasks((prev) =>
        prev.map((t) => ({ ...t, hasSecurityAudit: true }))
      );

      setMetrics((prev) => ({
        ...prev,
        securityScore: 100,
      }));

      const newCommit: GitCommitLog = {
        id: String(Date.now()),
        hash: Math.random().toString(16).substring(2, 9),
        message: 'sec(audit): automated OWASP check passed & credentials secured',
        timestamp: 'Just now',
        type: 'sec',
      };

      setCommits((prev) => [newCommit, ...prev]);
      addLog('Audit Complete: Security Health Score upgraded to 100%. No hardcoded secrets found!');
      setIsProcessing(false);
    }, 1200);
  };

  const handleGenerateTests = () => {
    setIsProcessing(true);
    addLog('Executing: Vitest TDD Test Generator for active tasks...');

    setTimeout(() => {
      setTasks((prev) =>
        prev.map((t) => (t.status === 'in_progress' ? { ...t, testStatus: 'passing' } : t))
      );

      setMetrics((prev) => ({
        ...prev,
        testCoverage: Math.min(100, prev.testCoverage + 5),
      }));

      addLog('TDD Generation Complete: Test coverage increased! All in-progress tests passed.');
      setIsProcessing(false);
    }, 1100);
  };

  const handleClearContext = () => {
    setMetrics((prev) => ({
      ...prev,
      contextTokenUsage: 12,
    }));
    addLog('Context Cleared: 3-Prompt Rule executed. Sesi chat di-reset menjadi 12% token usage.');
  };

  return (
    <div className="mx-auto max-w-5xl flex flex-col gap-6">
      
      {/* Top Banner */}
      <div className="rounded-2xl border border-purple-500/20 bg-gradient-to-r from-purple-950/40 via-slate-900 to-indigo-950/40 p-6 backdrop-blur-sm shadow-xl">
        <div className="flex items-center gap-3 mb-2">
          <Sparkles className="h-6 w-6 text-pink-400 animate-pulse" />
          <h2 className="text-lg font-bold text-white">AI Vibe Coding Assistant Simulator</h2>
        </div>
        <p className="text-xs text-slate-300 leading-relaxed">
          Simulasikan instruksi prompt Vibe Coding untuk melakukan otomatisasi task breakdown, audit keamanan kredensial, dan generasi pengujian unit test secara instan.
        </p>
      </div>

      {/* Quick Preset Action Buttons */}
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <button
          onClick={handleBreakdownFeature}
          disabled={isProcessing}
          className="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-900/80 p-4 text-left hover:border-indigo-500/40 hover:bg-slate-900 transition-all group"
        >
          <div className="rounded-lg bg-indigo-500/10 p-2.5 text-indigo-400 group-hover:scale-110 transition-transform">
            <Play className="h-4 w-4" />
          </div>
          <div>
            <div className="text-xs font-semibold text-white">Breakdown MVP Task</div>
            <div className="text-[11px] text-slate-400">Urai fitur ke sub-tugas</div>
          </div>
        </button>

        <button
          onClick={handleSecurityAudit}
          disabled={isProcessing}
          className="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-900/80 p-4 text-left hover:border-emerald-500/40 hover:bg-slate-900 transition-all group"
        >
          <div className="rounded-lg bg-emerald-500/10 p-2.5 text-emerald-400 group-hover:scale-110 transition-transform">
            <ShieldCheck className="h-4 w-4" />
          </div>
          <div>
            <div className="text-xs font-semibold text-white">Run Security Audit</div>
            <div className="text-[11px] text-slate-400">Pindai .env & credentials</div>
          </div>
        </button>

        <button
          onClick={handleGenerateTests}
          disabled={isProcessing}
          className="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-900/80 p-4 text-left hover:border-purple-500/40 hover:bg-slate-900 transition-all group"
        >
          <div className="rounded-lg bg-purple-500/10 p-2.5 text-purple-400 group-hover:scale-110 transition-transform">
            <CheckCircle2 className="h-4 w-4" />
          </div>
          <div>
            <div className="text-xs font-semibold text-white">Generate Vitest Suite</div>
            <div className="text-[11px] text-slate-400">TDD test automation</div>
          </div>
        </button>

        <button
          onClick={handleClearContext}
          disabled={isProcessing}
          className="flex items-center gap-3 rounded-xl border border-slate-800 bg-slate-900/80 p-4 text-left hover:border-pink-500/40 hover:bg-slate-900 transition-all group"
        >
          <div className="rounded-lg bg-pink-500/10 p-2.5 text-pink-400 group-hover:scale-110 transition-transform">
            <RefreshCw className="h-4 w-4" />
          </div>
          <div>
            <div className="text-xs font-semibold text-white">Clear Context Window</div>
            <div className="text-[11px] text-slate-400">Aturan 3-Prompt Reset</div>
          </div>
        </button>
      </div>

      {/* Terminal Log Console */}
      <div className="rounded-2xl border border-slate-800 bg-slate-950 p-5 shadow-2xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
          <div className="flex items-center gap-2">
            <Terminal className="h-4 w-4 text-slate-400" />
            <span className="text-xs font-mono font-semibold text-slate-200">AI Terminal Feed</span>
          </div>
          {isProcessing && (
            <span className="flex items-center gap-1.5 text-xs text-indigo-400 font-mono">
              <span className="h-2 w-2 rounded-full bg-indigo-400 animate-ping"></span>
              Executing prompt...
            </span>
          )}
        </div>

        <div className="flex flex-col gap-1.5 font-mono text-xs text-slate-300 max-h-60 overflow-y-auto">
          {logs.map((log, index) => (
            <div key={index} className="leading-relaxed">
              <span className="text-emerald-400">$&nbsp;</span>
              {log}
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};
