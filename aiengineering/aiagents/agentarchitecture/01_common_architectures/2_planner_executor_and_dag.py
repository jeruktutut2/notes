#!/usr/bin/env python3
"""
Modul 01: Common Architectures - Part 2
Simulasi Planner-Executor Agent & DAG (Directed Acyclic Graph) Agents
"""

import time
from collections import defaultdict, deque
from typing import List, Dict, Any

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


# ============================================================================
# 1. PLANNER-EXECUTOR AGENT WITH DYNAMIC REPLANNING
# ============================================================================
class PlannerExecutorAgent:
    """Agent yang memisahkan tahap perencanaan (Plan) dan eksekusi (Execute)."""

    def __init__(self):
        pass

    def create_plan(self, user_goal: str) -> List[Dict[str, Any]]:
        print(f"\n{YELLOW}[PLANNER AGENT]{RESET} Membuat rencana aksi awal untuk goal: '{user_goal}'...")
        plan = [
            {"step_id": 1, "description": "Fetch user transaction logs from database", "status": "PENDING"},
            {"step_id": 2, "description": "Analyze transaction logs for anomaly patterns", "status": "PENDING"},
            {"step_id": 3, "description": "Generate security alert summary PDF report", "status": "PENDING"}
        ]
        for step in plan:
            print(f"  • Step {step['step_id']}: {step['description']}")
        return plan

    def execute_plan(self, user_goal: str):
        print(f"\n{BOLD}{CYAN}=== PLANNER-EXECUTOR EXECUTION ==={RESET}")
        plan = self.create_plan(user_goal)

        print(f"\n{GREEN}[EXECUTOR AGENT]{RESET} Memulai eksekusi langkah berurutan...")
        for i, step in enumerate(plan):
            print(f"\nMenjalankan Step #{step['step_id']}: '{step['description']}'")
            
            # Simulasi kegagalan pada step 2 untuk memicu Dynamic Replanning
            if step["step_id"] == 2 and not step.get("retried"):
                print(f"  {RED}[ERROR] Gagal menganalisis transaksi: Format log tidak valid.{RESET}")
                print(f"  {MAGENTA}[REPLANNER TRIGGERED]{RESET} Mengirimkan feedback ke Planner untuk penyesuaian plan...")
                
                # Dynamic Replanning
                print(f"  {YELLOW}[RE-PLANNING]{RESET} Memperbaiki rencana: Menambahkan 'Normalize Log Format' sebelum analisis.")
                new_sub_steps = [
                    {"step_id": "2a", "description": "Normalize log format to JSON standard", "status": "COMPLETED"},
                    {"step_id": "2b", "description": "Analyze transaction logs for anomaly patterns", "status": "COMPLETED", "retried": True}
                ]
                print(f"  {GREEN}[EXECUTOR]{RESET} Menjalankan langkah perbaikan (Step 2a & 2b)... Selesai!")
                step["status"] = "COMPLETED"
            else:
                print(f"  {GREEN}[SUCCESS]{RESET} Step #{step['step_id']} berhasil dieksekusi.")
                step["status"] = "COMPLETED"

        print(f"\n{BOLD}{GREEN}✓ Seluruh Rencana Berhasil Diselesaikan!{RESET}")


# ============================================================================
# 2. DAG AGENTS (Directed Acyclic Graph Execution Engine)
# ============================================================================
class DAGTask:
    def __init__(self, task_id: str, description: str, dependencies: List[str] = None):
        self.task_id = task_id
        self.description = description
        self.dependencies = dependencies or []
        self.result = None


class DAGAgentEngine:
    """Mesin eksekusi Agent berbasis Graf Terarah Tanpa Siklus (DAG)."""

    def __init__(self):
        self.tasks: Dict[str, DAGTask] = {}

    def add_task(self, task: DAGTask):
        self.tasks[task.task_id] = task

    def execute_dag(self):
        print(f"\n{BOLD}{MAGENTA}=== DAG AGENT ENGINE EXECUTION ==={RESET}")
        print(f"Menganalisis Graf Dependensi Tugas ({len(self.tasks)} node)...")

        # Topo sort / Level-based parallel execution grouping
        in_degree = {t_id: len(task.dependencies) for t_id, task in self.tasks.items()}
        graph = defaultdict(list)
        for t_id, task in self.tasks.items():
            for dep in task.dependencies:
                graph[dep].append(t_id)

        queue = deque([t_id for t_id, deg in in_degree.items() if deg == 0])
        execution_batches = []

        while queue:
            batch = list(queue)
            execution_batches.append(batch)
            queue.clear()

            for t_id in batch:
                for neighbor in graph[t_id]:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)

        # Print execution structure
        for level, batch in enumerate(execution_batches, 1):
            tasks_str = ", ".join(batch)
            print(f"\n{BOLD}Level {level} (Parallel Batch): [{tasks_str}]{RESET}")
            for t_id in batch:
                task = self.tasks[t_id]
                deps_str = f"(Dependencies: {task.dependencies})" if task.dependencies else "(No dependencies)"
                print(f"  ⚡ Eksekusi Node [{t_id}]: {task.description} {BLUE}{deps_str}{RESET}")
                task.result = f"Output_Data_{t_id}"
                print(f"     -> Result: {GREEN}SUCCESS ({task.result}){RESET}")

        print(f"\n{BOLD}{GREEN}✓ DAG Execution Graph Completed Successfully!{RESET}")


# ============================================================================
# DEMO EXECUTION
# ============================================================================
def main():
    print(f"{BOLD}{GREEN}===================================================={RESET}")
    print(f"{BOLD}{GREEN} MODUL 01.2: PLANNER-EXECUTOR & DAG AGENTS         {RESET}")
    print(f"{BOLD}{GREEN}===================================================={RESET}")

    # Demo 1: Planner-Executor Agent
    planner = PlannerExecutorAgent()
    planner.execute_plan("Deteksi Anomali Keamanan Transaksi Finansial")

    # Demo 2: DAG Agents
    dag_engine = DAGAgentEngine()
    
    # Node 1: Fetch raw sales & inventory
    dag_engine.add_task(DAGTask("T1", "Fetch Raw Sales Data"))
    dag_engine.add_task(DAGTask("T2", "Fetch Inventory DB"))
    
    # Node 2 (Depends on T1 / T2): Analysis (Can run in parallel after T1 & T2)
    dag_engine.add_task(DAGTask("T3", "Calculate Sales Revenue", dependencies=["T1"]))
    dag_engine.add_task(DAGTask("T4", "Calculate Stock Depletion Rate", dependencies=["T1", "T2"]))
    
    # Node 3 (Depends on T3 & T4): Synthesis Report
    dag_engine.add_task(DAGTask("T5", "Compile Final Executive Dashboard", dependencies=["T3", "T4"]))

    dag_engine.execute_dag()


if __name__ == "__main__":
    main()
