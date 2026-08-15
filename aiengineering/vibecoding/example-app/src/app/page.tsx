'use client';

import React, { useState, useEffect } from 'react';
import { Task, TaskStatus, VibeMetrics, GitCommitLog } from '@/types/vibe';
import { INITIAL_TASKS, INITIAL_METRICS, INITIAL_COMMITS } from '@/data/initialData';
import { Header } from '@/components/Header';
import { KanbanBoard } from '@/components/KanbanBoard';
import { PrdViewer } from '@/components/PrdViewer';
import { AiSimulator } from '@/components/AiSimulator';
import { MetricsDashboard } from '@/components/MetricsDashboard';
import { TaskModal } from '@/components/TaskModal';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'kanban' | 'prd' | 'ai' | 'metrics'>('kanban');
  const [searchQuery, setSearchQuery] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  // LocalStorage Persistence
  const [tasks, setTasks] = useState<Task[]>(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('vibeflow_tasks');
      if (saved) {
        try {
          return JSON.parse(saved);
        } catch (e) {
          console.error(e);
        }
      }
    }
    return INITIAL_TASKS;
  });

  const [metrics, setMetrics] = useState<VibeMetrics>(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('vibeflow_metrics');
      if (saved) {
        try {
          return JSON.parse(saved);
        } catch (e) {
          console.error(e);
        }
      }
    }
    return INITIAL_METRICS;
  });

  const [commits, setCommits] = useState<GitCommitLog[]>(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('vibeflow_commits');
      if (saved) {
        try {
          return JSON.parse(saved);
        } catch (e) {
          console.error(e);
        }
      }
    }
    return INITIAL_COMMITS;
  });

  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('vibeflow_tasks', JSON.stringify(tasks));
    }
  }, [tasks]);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('vibeflow_metrics', JSON.stringify(metrics));
    }
  }, [metrics]);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('vibeflow_commits', JSON.stringify(commits));
    }
  }, [commits]);

  const handleMoveStatus = (id: string, newStatus: TaskStatus) => {
    setTasks((prev) =>
      prev.map((t) => (t.id === id ? { ...t, status: newStatus } : t))
    );

    if (newStatus === 'done') {
      setMetrics((prev) => ({
        ...prev,
        commitCount: prev.commitCount + 1,
      }));
    }
  };

  const handleDeleteTask = (id: string) => {
    setTasks((prev) => prev.filter((t) => t.id !== id));
  };

  const handleCreateTask = (newTaskData: Omit<Task, 'id' | 'createdAt'>) => {
    const newTask: Task = {
      ...newTaskData,
      id: `TASK-${Math.floor(100 + Math.random() * 900)}`,
      createdAt: new Date().toISOString().slice(0, 16).replace('T', ' '),
    };

    setTasks((prev) => [newTask, ...prev]);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-indigo-500 selection:text-white">
      
      {/* Sticky Header */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        onOpenCreateModal={() => setIsModalOpen(true)}
        taskCount={tasks.length}
      />

      {/* Main Container */}
      <main className="mx-auto max-w-7xl px-4 py-8 md:px-8">
        {activeTab === 'kanban' && (
          <KanbanBoard
            tasks={tasks}
            onMoveStatus={handleMoveStatus}
            onDeleteTask={handleDeleteTask}
            searchQuery={searchQuery}
          />
        )}

        {activeTab === 'prd' && <PrdViewer />}

        {activeTab === 'ai' && (
          <AiSimulator
            tasks={tasks}
            setTasks={setTasks}
            metrics={metrics}
            setMetrics={setMetrics}
            setCommits={setCommits}
          />
        )}

        {activeTab === 'metrics' && (
          <MetricsDashboard metrics={metrics} commits={commits} />
        )}
      </main>

      {/* Modal */}
      <TaskModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onCreateTask={handleCreateTask}
      />

      {/* Footer */}
      <footer className="mt-12 border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <p>VibeFlow v1.0.0 — Crafted with Next.js & TailwindCSS for Vibe Coding Methodology</p>
      </footer>

    </div>
  );
}
