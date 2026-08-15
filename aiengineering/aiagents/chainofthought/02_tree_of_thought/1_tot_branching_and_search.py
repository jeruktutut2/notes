#!/usr/bin/env python3
"""
SIMULASI MODUL 2.1: Tree of Thought (ToT) Branching & Search Algorithms (BFS vs DFS)
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents)

Modul ini mensimulasikan arsitektur Tree of Thought (Yao et al., 2023) tempat agen
menghasilkan beberapa cabang pemikiran paralel (branching factor k) dan menjelajahinya
menggunakan algoritma Breadth-First Search (BFS) atau Depth-First Search (DFS).
"""

import time
from dataclasses import dataclass, field
from typing import List, Optional, Dict

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

@dataclass
class ThoughtNode:
    id: str
    thought_content: str
    depth: int
    score: float = 0.0  # Heuristic / Evaluator score (0.0 to 1.0)
    children: List['ThoughtNode'] = field(default_factory=list)
    parent: Optional['ThoughtNode'] = None
    is_terminal: bool = False

def build_sample_thought_tree() -> ThoughtNode:
    """
    Membangun pohon pemikiran contoh untuk studi kasus menyusun rencana arsitektur sistem
    """
    root = ThoughtNode("Node-0", "Tugas: Desain arsitektur database untuk aplikasi e-commerce 10M pengguna", depth=0, score=1.0)
    
    # Depth 1 Branches (Branching factor k=3)
    b1 = ThoughtNode("Node-1.1", "Opsi A: Gunakan Monolithic Single PostgreSQL DB dengan Read Replicas", depth=1, score=0.4)
    b2 = ThoughtNode("Node-1.2", "Opsi B: Gunakan Microservices DB per Service (User, Order, Inventory DB)", depth=1, score=0.85)
    b3 = ThoughtNode("Node-1.3", "Opsi C: Gunakan Pure NoSQL Document DB (MongoDB)", depth=1, score=0.5)
    
    root.children = [b1, b2, b3]
    b1.parent = root
    b2.parent = root
    b3.parent = root
    
    # Sub-branches for Node-1.2 (Microservices)
    b2_1 = ThoughtNode("Node-2.1", "Microservices + CQRS & Event Sourcing (Kafka)", depth=2, score=0.92, is_terminal=True)
    b2_2 = ThoughtNode("Node-2.2", "Microservices + Direct REST Sync Calls antar service", depth=2, score=0.45, is_terminal=True)
    
    b2.children = [b2_1, b2_2]
    b2_1.parent = b2
    b2_2.parent = b2
    
    # Sub-branches for Node-1.1 (Monolith)
    b1_1 = ThoughtNode("Node-2.3", "Monolith + Redis Cache layer untuk katalog produk", depth=2, score=0.6, is_terminal=True)
    b1.children = [b1_1]
    b1_1.parent = b1
    
    return root

def print_tree_visually(node: ThoughtNode, prefix: str = "", is_last: bool = True):
    connector = "└── " if is_last else "├── "
    color = GREEN if node.score >= 0.8 else (YELLOW if node.score >= 0.5 else RED)
    
    print(f"{prefix}{connector}{BOLD}{node.id}{RESET} [{color}Score: {node.score:.2f}{RESET}] : {node.thought_content}")
    
    new_prefix = prefix + ("    " if is_last else "│   ")
    for i, child in enumerate(node.children):
        print_tree_visually(child, new_prefix, i == len(node.children) - 1)

def explore_bfs(root: ThoughtNode):
    print(f"\n{BOLD}{CYAN}=== EKSPLORASI TREE OF THOUGHT MENGGUNAKAN BFS (Breadth-First Search) ==={RESET}\n")
    queue = [root]
    visited = []
    
    step = 1
    while queue:
        current = queue.pop(0)
        visited.append(current)
        print(f"Step {step}: Mengunjungi {BOLD}{current.id}{RESET} (Depth {current.depth}) - Score: {current.score:.2f}")
        print(f"  💭 Thought: {current.thought_content}")
        time.sleep(0.2)
        
        for child in current.children:
            queue.append(child)
        step += 1

def explore_dfs(root: ThoughtNode):
    print(f"\n{BOLD}{MAGENTA}=== EKSPLORASI TREE OF THOUGHT MENGGUNAKAN DFS (Depth-First Search) ==={RESET}\n")
    stack = [root]
    visited = []
    
    step = 1
    while stack:
        current = stack.pop()
        visited.append(current)
        print(f"Step {step}: Mengunjungi {BOLD}{current.id}{RESET} (Depth {current.depth}) - Score: {current.score:.2f}")
        print(f"  💭 Thought: {current.thought_content}")
        time.sleep(0.2)
        
        # Push children in reverse to explore leftmost first
        for child in reversed(current.children):
            stack.append(child)
        step += 1

def main():
    print(f"\n{BOLD}{GREEN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}      SIMULASI TREE OF THOUGHT (ToT): BRANCHING & SEARCH ALGORITHMS    {RESET}")
    print(f"{BOLD}{GREEN}======================================================================{RESET}")
    
    tree_root = build_sample_thought_tree()
    
    print(f"\n{BOLD}{YELLOW}POHON PEMIKIRAN (TREE OF THOUGHT STRUCTURE):{RESET}\n")
    print_tree_visually(tree_root)
    
    input(f"\n{YELLOW}Tekan [Enter] untuk menjalankan simulasi eksplorasi BFS...{RESET}")
    explore_bfs(tree_root)
    
    input(f"\n{YELLOW}Tekan [Enter] untuk menjalankan simulasi eksplorasi DFS...{RESET}")
    explore_dfs(tree_root)
    
    print(f"\n{BOLD}{GREEN}✓ Simulasi ToT Search Selesai!{RESET}\n")

if __name__ == "__main__":
    main()
