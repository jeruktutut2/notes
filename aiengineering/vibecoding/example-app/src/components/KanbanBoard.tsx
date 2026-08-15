'use client';

import React, { useState } from 'react';
import { Task, TaskStatus, TaskCategory } from '@/types/vibe';
import { TaskCard } from './TaskCard';
import { Circle, Clock3, Eye, CheckCircle, Filter } from 'lucide-react';

interface KanbanBoardProps {
  tasks: Task[];
  onMoveStatus: (id: string, newStatus: TaskStatus) => void;
  onDeleteTask: (id: string) => void;
  searchQuery: string;
}

export const KanbanBoard: React.FC<KanbanBoardProps> = ({
  tasks,
  onMoveStatus,
  onDeleteTask,
  searchQuery,
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  const filteredTasks = tasks.filter((task) => {
    const matchesSearch =
      task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      task.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      task.id.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesCategory =
      selectedCategory === 'all' || task.category === selectedCategory;

    return matchesSearch && matchesCategory;
  });

  const columns: { id: TaskStatus; title: string; icon: React.ReactNode; color: string }[] = [
    {
      id: 'todo',
      title: 'To Do',
      icon: <Circle className="h-4 w-4 text-slate-400" />,
      color: 'border-slate-800 bg-slate-900/40',
    },
    {
      id: 'in_progress',
      title: 'In Progress',
      icon: <Clock3 className="h-4 w-4 text-indigo-400" />,
      color: 'border-indigo-500/20 bg-indigo-950/20',
    },
    {
      id: 'review',
      title: 'Review / TDD Audit',
      icon: <Eye className="h-4 w-4 text-purple-400" />,
      color: 'border-purple-500/20 bg-purple-950/20',
    },
    {
      id: 'done',
      title: 'Done',
      icon: <CheckCircle className="h-4 w-4 text-emerald-400" />,
      color: 'border-emerald-500/20 bg-emerald-950/20',
    },
  ];

  const categories: { key: string; label: string }[] = [
    { key: 'all', label: 'Semua Category' },
    { key: 'feature', label: 'Feature' },
    { key: 'bugfix', label: 'Bugfix' },
    { key: 'tdd', label: 'TDD Test' },
    { key: 'security', label: 'Security' },
    { key: 'refactor', label: 'Refactor' },
  ];

  return (
    <div className="flex flex-col gap-6">
      
      {/* Category Filter Pills */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1">
        <Filter className="h-4 w-4 text-slate-400 shrink-0 ml-1" />
        <div className="flex items-center gap-1.5">
          {categories.map((cat) => (
            <button
              key={cat.key}
              onClick={() => setSelectedCategory(cat.key)}
              className={`rounded-lg px-3 py-1 text-xs font-medium transition-all ${
                selectedCategory === cat.key
                  ? 'bg-slate-800 text-indigo-400 border border-indigo-500/30'
                  : 'bg-slate-900/60 text-slate-400 border border-slate-800 hover:text-slate-200'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      {/* 4 Columns Board */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
        {columns.map((col) => {
          const colTasks = filteredTasks.filter((t) => t.status === col.id);

          return (
            <div
              key={col.id}
              className={`flex flex-col rounded-2xl border p-4 backdrop-blur-sm min-h-[500px] ${col.color}`}
            >
              {/* Column Header */}
              <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-800">
                <div className="flex items-center gap-2">
                  {col.icon}
                  <h2 className="text-sm font-bold text-white">{col.title}</h2>
                </div>
                <span className="rounded-full bg-slate-800 px-2 py-0.5 text-xs font-semibold text-slate-300">
                  {colTasks.length}
                </span>
              </div>

              {/* Task Card Items */}
              <div className="flex flex-1 flex-col gap-3">
                {colTasks.length === 0 ? (
                  <div className="flex flex-1 items-center justify-center rounded-xl border border-dashed border-slate-800 p-6 text-center">
                    <p className="text-xs text-slate-500">Tidak ada tugas di kolom ini</p>
                  </div>
                ) : (
                  colTasks.map((task) => (
                    <TaskCard
                      key={task.id}
                      task={task}
                      onMoveStatus={onMoveStatus}
                      onDelete={onDeleteTask}
                    />
                  ))
                )}
              </div>

            </div>
          );
        })}
      </div>

    </div>
  );
};
