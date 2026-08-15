'use client';

import React from 'react';
import { Task, TaskStatus } from '@/types/vibe';
import { 
  CheckCircle2, 
  XCircle, 
  Clock, 
  ShieldCheck, 
  ShieldAlert, 
  ArrowRight, 
  ArrowLeft, 
  Trash2,
  Tag
} from 'lucide-react';

interface TaskCardProps {
  task: Task;
  onMoveStatus: (id: string, newStatus: TaskStatus) => void;
  onDelete: (id: string) => void;
}

export const TaskCard: React.FC<TaskCardProps> = ({ task, onMoveStatus, onDelete }) => {
  const getPriorityColor = (p: string) => {
    switch (p) {
      case 'high': return 'bg-rose-500/10 text-rose-400 border-rose-500/20';
      case 'medium': return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
      case 'low': return 'bg-blue-500/10 text-blue-400 border-blue-500/20';
      default: return 'bg-slate-800 text-slate-400';
    }
  };

  const getCategoryBadge = (c: string) => {
    switch (c) {
      case 'feature': return 'bg-indigo-500/15 text-indigo-300 border-indigo-500/30';
      case 'bugfix': return 'bg-rose-500/15 text-rose-300 border-rose-500/30';
      case 'tdd': return 'bg-purple-500/15 text-purple-300 border-purple-500/30';
      case 'security': return 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30';
      case 'refactor': return 'bg-amber-500/15 text-amber-300 border-amber-500/30';
      default: return 'bg-slate-800 text-slate-300';
    }
  };

  const getTestBadge = (status: string) => {
    switch (status) {
      case 'passing':
        return (
          <span className="flex items-center gap-1 text-[11px] font-medium text-emerald-400">
            <CheckCircle2 className="h-3.5 w-3.5" />
            <span>Test Pass</span>
          </span>
        );
      case 'failing':
        return (
          <span className="flex items-center gap-1 text-[11px] font-medium text-rose-400">
            <XCircle className="h-3.5 w-3.5" />
            <span>Test Fail</span>
          </span>
        );
      default:
        return (
          <span className="flex items-center gap-1 text-[11px] font-medium text-slate-400">
            <Clock className="h-3.5 w-3.5" />
            <span>No Test</span>
          </span>
        );
    }
  };

  const getNextStatus = (current: TaskStatus): TaskStatus | null => {
    if (current === 'todo') return 'in_progress';
    if (current === 'in_progress') return 'review';
    if (current === 'review') return 'done';
    return null;
  };

  const getPrevStatus = (current: TaskStatus): TaskStatus | null => {
    if (current === 'done') return 'review';
    if (current === 'review') return 'in_progress';
    if (current === 'in_progress') return 'todo';
    return null;
  };

  const nextStatus = getNextStatus(task.status);
  const prevStatus = getPrevStatus(task.status);

  return (
    <div className="group relative flex flex-col justify-between rounded-xl border border-slate-800 bg-slate-900/80 p-4 transition-all duration-200 hover:border-slate-700 hover:bg-slate-900 hover:shadow-xl hover:shadow-indigo-500/5">
      
      {/* Top Meta Bar */}
      <div>
        <div className="flex items-center justify-between gap-2 mb-2">
          <span className="text-[11px] font-mono font-medium text-slate-400">
            {task.id}
          </span>
          <div className="flex items-center gap-1.5">
            <span className={`rounded-md border px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider ${getPriorityColor(task.priority)}`}>
              {task.priority}
            </span>
            <button
              onClick={() => onDelete(task.id)}
              className="text-slate-500 opacity-0 transition-opacity hover:text-rose-400 group-hover:opacity-100 p-0.5"
              title="Hapus tugas"
            >
              <Trash2 className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>

        {/* Task Title & Description */}
        <h3 className="text-sm font-semibold text-slate-100 leading-snug mb-1">
          {task.title}
        </h3>
        <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-3">
          {task.description}
        </p>

        {/* Badges & Tags */}
        <div className="flex flex-wrap items-center gap-2 mb-3">
          <span className={`flex items-center gap-1 rounded-md border px-2 py-0.5 text-[10px] font-medium uppercase ${getCategoryBadge(task.category)}`}>
            <Tag className="h-3 w-3" />
            {task.category}
          </span>

          {task.hasSecurityAudit ? (
            <span className="flex items-center gap-1 rounded-md border border-emerald-500/20 bg-emerald-500/10 px-2 py-0.5 text-[10px] font-medium text-emerald-400" title="Security Audited">
              <ShieldCheck className="h-3 w-3" />
              <span>Audited</span>
            </span>
          ) : (
            <span className="flex items-center gap-1 rounded-md border border-slate-700 bg-slate-800/50 px-2 py-0.5 text-[10px] font-medium text-slate-400" title="Needs Audit">
              <ShieldAlert className="h-3 w-3 text-amber-400" />
              <span>Pending Audit</span>
            </span>
          )}
        </div>
      </div>

      {/* Bottom Bar & Quick Status Movers */}
      <div className="flex items-center justify-between pt-2 border-t border-slate-800/80">
        <div>{getTestBadge(task.testStatus)}</div>

        <div className="flex items-center gap-1">
          {prevStatus && (
            <button
              onClick={() => onMoveStatus(task.id, prevStatus)}
              className="flex items-center justify-center rounded-lg border border-slate-800 bg-slate-950 p-1 text-slate-400 hover:border-slate-700 hover:text-white transition-all"
              title={`Mundur ke ${prevStatus}`}
            >
              <ArrowLeft className="h-3.5 w-3.5" />
            </button>
          )}

          {nextStatus && (
            <button
              onClick={() => onMoveStatus(task.id, nextStatus)}
              className="flex items-center gap-1 rounded-lg border border-indigo-500/30 bg-indigo-600/20 px-2 py-1 text-[11px] font-medium text-indigo-300 hover:bg-indigo-600/30 transition-all"
              title={`Maju ke ${nextStatus}`}
            >
              <span>Lanjut</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </button>
          )}
        </div>
      </div>

    </div>
  );
};
