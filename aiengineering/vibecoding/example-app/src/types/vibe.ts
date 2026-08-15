export type TaskStatus = 'todo' | 'in_progress' | 'review' | 'done';
export type TaskPriority = 'low' | 'medium' | 'high';
export type TaskCategory = 'feature' | 'bugfix' | 'tdd' | 'security' | 'refactor';
export type TestStatus = 'passing' | 'failing' | 'pending';

export interface Task {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  priority: TaskPriority;
  category: TaskCategory;
  testStatus: TestStatus;
  hasSecurityAudit: boolean;
  createdAt: string;
}

export interface VibeMetrics {
  testCoverage: number; // 0 to 100
  securityScore: number; // 0 to 100
  contextTokenUsage: number; // 0 to 100
  commitCount: number;
}

export interface GitCommitLog {
  id: string;
  hash: string;
  message: string;
  timestamp: string;
  type: 'feat' | 'fix' | 'test' | 'sec' | 'refactor';
}
