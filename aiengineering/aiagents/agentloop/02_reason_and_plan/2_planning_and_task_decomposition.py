#!/usr/bin/env python3
"""
Modul 2.2: Task Decomposition & DAG Planning
Demonstrasi bagaimana AI Agent memecah tugas kompleks menjadi rencana terstruktur (Sub-tasks DAG)
lengkap dengan status dependensi antar langkah sebelum mengeksekusinya.
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field

# ANSI Terminal Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

@dataclass
class TaskNode:
    id: str
    description: str
    dependencies: List[str]
    status: str = "PENDING"  # PENDING, IN_PROGRESS, COMPLETED, FAILED
    result: Any = None

class DAGPlanner:
    def __init__(self, main_goal: str):
        self.main_goal = main_goal
        self.tasks: Dict[str, TaskNode] = {}

    def decompose_goal(self):
        """Memecah goal utama menjadi grafik tugas (DAG Task Graph)."""
        print(f" Memecah goal utama: '{self.main_goal}'...")
        
        t1 = TaskNode("T1", "Ambil data transaksi dari API", dependencies=[])
        t2 = TaskNode("T2", "Bersihkan & hilangkan outlier data", dependencies=["T1"])
        t3 = TaskNode("T3", "Hitung statistik deskriptif data", dependencies=["T2"])
        t4 = TaskNode("T4", "Generate file grafik visualisasi PNG", dependencies=["T2"])
        t5 = TaskNode("T5", "Kirim ringkasan laporan via Email", dependencies=["T3", "T4"])

        for task in [t1, t2, t3, t4, t5]:
            self.tasks[task.id] = task

    def get_executable_tasks(self) -> List[TaskNode]:
        """Mengembalikan daftar tugas yang siap dieksekusi (seluruh dependensinya sudah COMPLETED)."""
        executable = []
        for task in self.tasks.values():
            if task.status == "PENDING":
                deps_satisfied = all(self.tasks[dep_id].status == "COMPLETED" for dep_id in task.dependencies)
                if deps_satisfied:
                    executable.append(task)
        return executable

def main():
    print(f"\n{BOLD}{CYAN}=== MODUL 2.2: TASK DECOMPOSITION & DAG PLANNING ==={RESET}\n")

    goal = "Buat laporan analisis penjualan kuartalan beserta grafik visualisasi"
    planner = DAGPlanner(main_goal=goal)
    planner.decompose_goal()

    print(f"\n{BOLD}Grafik Rencana Tugas (Task Graph):{RESET}")
    for task in planner.tasks.values():
        deps_str = ", ".join(task.dependencies) if task.dependencies else "Tidak ada"
        print(f"  • [{BOLD}{task.id}{RESET}] {task.description} (Dep: {deps_str})")

    print(f"\n{BOLD}Simulasi Eksekusi Berdasarkan Dependensi:{RESET}\n")

    step = 1
    while True:
        ready_tasks = planner.get_executable_tasks()
        if not ready_tasks:
            break

        print(f"{BOLD}{BLUE}--- Iterasi Perencanaan Step #{step} ---{RESET}")
        print(f"Tugas yang Siap Dieksekusi Saat Ini:")
        for t in ready_tasks:
            print(f"  -> Executing [{BOLD}{t.id}{RESET}]: {t.description}")
            t.status = "COMPLETED"
            t.result = f"OK_{t.id}"
            print(f"     Status: {GREEN}COMPLETED{RESET}")
        step += 1
        print("-" * 55)

    all_done = all(t.status == "COMPLETED" for t in planner.tasks.values())
    if all_done:
        print(f"\n{GREEN}{BOLD}🎉 Seluruh sub-tugas dalam DAG Plan berhasil diselesaikan!{RESET}\n")

if __name__ == "__main__":
    main()
