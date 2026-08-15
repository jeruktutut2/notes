#!/usr/bin/env python3
"""
Modul 2.2: Sandboxed Execution Environment
Simulasi lingkungan eksekusi kode terisolasi (AST Validator & Directory Jail)
untuk mencegah eksekusi modul berbahaya dan pembacaan file di luar direktori sah.
"""

import ast
import os
from typing import Tuple, List

# ANSI Color formatting
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


class ASTSandboxValidator(ast.NodeVisitor):
    """AST Inspector untuk mendeteksi perintah/import berbahaya sebelum kode dijalankan."""

    FORBIDDEN_MODULES = {"os", "sys", "subprocess", "shutil", "socket", "ctypes", "builtins"}
    FORBIDDEN_FUNCTIONS = {"eval", "exec", "open", "__import__"}

    def __init__(self):
        self.violations: List[str] = []

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            if alias.name.split('.')[0] in self.FORBIDDEN_MODULES:
                self.violations.append(f"Import modul terlarang: '{alias.name}'")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module and node.module.split('.')[0] in self.FORBIDDEN_MODULES:
            self.violations.append(f"ImportFrom modul terlarang: '{node.module}'")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in self.FORBIDDEN_FUNCTIONS:
            self.violations.append(f"Pemanggilan fungsi terlarang: '{node.func.id}()'")
        self.generic_visit(node)


class SandboxRunner:
    """Runner eksekusi terisolasi yang menguji AST dan mengunci akses file path."""

    def __init__(self, allowed_workspace: str = "/app/sandbox"):
        self.allowed_workspace = os.path.abspath(allowed_workspace)

    def validate_code_safety(self, code_str: str) -> Tuple[bool, List[str]]:
        """Memeriksa keamanan sintaksis kode Python menggunakan AST Analysis."""
        try:
            tree = ast.parse(code_str)
            validator = ASTSandboxValidator()
            validator.visit(tree)
            if validator.violations:
                return False, validator.violations
            return True, []
        except SyntaxError as e:
            return False, [f"Syntax Error: {e}"]

    def validate_file_path(self, target_path: str) -> Tuple[bool, str]:
        """Directory Traversal Jail Check: Memastikan file berada di dalam workspace terisolasi."""
        absolute_target = os.path.abspath(os.path.join(self.allowed_workspace, target_path))
        if not absolute_target.startswith(self.allowed_workspace):
            return False, f"Directory Traversal Disertai Jailbreak Attempt: Target '{target_path}' berada di luar workspace '{self.allowed_workspace}'!"
        return True, f"Path aman: {absolute_target}"

    def execute_safe_python(self, code_str: str) -> str:
        """Menjalankan kode Python jika lolos inspeksi AST."""
        is_safe, violations = self.validate_code_safety(code_str)
        if not is_safe:
            return f"{RED}[SANDBOX BLOCKED]: Kode ditolak! Pelanggaran keamanan:\n- " + "\n- ".join(violations) + f"{RESET}"

        # Simulasi eksekusi dalam namespace terisolasi
        try:
            safe_globals = {"__builtins__": {"print": print, "range": range, "len": len, "sum": sum, "max": max}}
            safe_locals = {}
            exec(code_str, safe_globals, safe_locals)
            return f"{GREEN}[SANDBOX EXECUTION SUCCESS]: Kode berhasil dieksekusi tanpa pelanggaran safety.{RESET}"
        except Exception as e:
            return f"{RED}[EXECUTION ERROR]: {e}{RESET}"


def main():
    print(f"\n{BOLD}{CYAN}=== DEMO 2.2: SANDBOXED EXECUTION ENVIRONMENT ==={RESET}\n")

    sandbox = SandboxRunner(allowed_workspace="/app/sandbox")

    # 1. Menguji Kode Berbahaya (Malicious Import & Sys Call)
    print(f"{BOLD}[1] UJI KODE PERINTAH BERBAHAYA (OS/SUBPROCESS IMPORT){RESET}")
    malicious_code = """
import os
import subprocess

os.system("rm -rf /")
print("Hacked!")
"""
    print(f"Kode yang diajukan Agent:\n{YELLOW}{malicious_code.strip()}{RESET}")
    print(sandbox.execute_safe_python(malicious_code))
    print()

    # 2. Menguji Kode Aman (Matematika & Pemrosesan Data)
    print(f"{BOLD}[2] UJI KODE AMAN (PENJUMLAHAN & AGREGASI DATA){RESET}")
    safe_code = """
numbers = [10, 25, 30, 45]
total = sum(numbers)
print(f"Hasil perhitungan total: {total}")
"""
    print(f"Kode yang diajukan Agent:\n{YELLOW}{safe_code.strip()}{RESET}")
    print(sandbox.execute_safe_python(safe_code))
    print()

    # 3. Menguji Path Traversal Jail Check (File System Access)
    print(f"{BOLD}[3] UJI DIRECTORY TRAVERSAL JAIL CHECK{RESET}")
    print(f"Allowed Workspace: {CYAN}/app/sandbox{RESET}")
    
    valid_file = "data/reports.json"
    print(f"-> Agent meminta akses file: '{valid_file}'")
    is_ok, msg = sandbox.validate_file_path(valid_file)
    print(f"Result: {GREEN if is_ok else RED}{msg}{RESET}")

    exploit_file = "../../../etc/passwd"
    print(f"-> Agent (terkontaminasi) meminta akses file: '{exploit_file}'")
    is_ok, msg = sandbox.validate_file_path(exploit_file)
    print(f"Result: {GREEN if is_ok else RED}{msg}{RESET}\n")

    print(f"{BOLD}{GREEN}✔ Simulasi Modul 2.2 Selesai.{RESET}\n")


if __name__ == "__main__":
    main()
