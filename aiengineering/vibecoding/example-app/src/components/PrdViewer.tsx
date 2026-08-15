'use client';

import React, { useState } from 'react';
import { PRD_CONTENT, AGENTS_CONTENT } from '@/data/initialData';
import { FileText, Shield, Copy, Check, Download } from 'lucide-react';

export const PrdViewer: React.FC = () => {
  const [activeDoc, setActiveDoc] = useState<'prd' | 'agents'>('prd');
  const [copied, setCopied] = useState(false);

  const content = activeDoc === 'prd' ? PRD_CONTENT : AGENTS_CONTENT;
  const fileName = activeDoc === 'prd' ? 'PRD.md' : 'AGENTS.md';

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="mx-auto max-w-5xl rounded-2xl border border-slate-800 bg-slate-900/80 backdrop-blur-sm p-6 shadow-2xl">
      
      {/* Tab Switcher & Actions */}
      <div className="flex flex-col gap-4 border-b border-slate-800 pb-4 md:flex-row md:items-center md:justify-between">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveDoc('prd')}
            className={`flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-semibold transition-all ${
              activeDoc === 'prd'
                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
                : 'bg-slate-800/60 text-slate-400 hover:text-slate-200'
            }`}
          >
            <FileText className="h-4 w-4" />
            <span>PRD.md (Product Specs)</span>
          </button>

          <button
            onClick={() => setActiveDoc('agents')}
            className={`flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-semibold transition-all ${
              activeDoc === 'agents'
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-600/30'
                : 'bg-slate-800/60 text-slate-400 hover:text-slate-200'
            }`}
          >
            <Shield className="h-4 w-4 text-purple-400" />
            <span>AGENTS.md (Style Rules)</span>
          </button>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className="flex items-center gap-1.5 rounded-lg border border-slate-800 bg-slate-950 px-3 py-1.5 text-xs font-medium text-slate-300 hover:border-slate-700 hover:text-white transition-all"
          >
            {copied ? <Check className="h-4 w-4 text-emerald-400" /> : <Copy className="h-4 w-4" />}
            <span>{copied ? 'Tersalin!' : 'Salin Markdown'}</span>
          </button>

          <button
            onClick={handleDownload}
            className="flex items-center gap-1.5 rounded-lg border border-indigo-500/30 bg-indigo-600/20 px-3 py-1.5 text-xs font-medium text-indigo-300 hover:bg-indigo-600/30 transition-all"
          >
            <Download className="h-4 w-4" />
            <span>Unduh {fileName}</span>
          </button>
        </div>
      </div>

      {/* Markdown Content Display */}
      <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950 p-6 overflow-x-auto">
        <pre className="whitespace-pre-wrap font-mono text-xs text-slate-300 leading-relaxed">
          {content}
        </pre>
      </div>

    </div>
  );
};
