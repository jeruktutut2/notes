#!/usr/bin/env python3
"""
Modul 2.1: Tool Permission & RBAC (Role-Based Access Control)
Simulasi kontrol hak akses tool berdasarkan peran pengguna (Guest vs User vs Admin)
dan konfirmasi manusia (Human-in-the-Loop / HITL) untuk aksi sensitif.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Any, Callable

# ANSI Color formatting
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


class UserRole(Enum):
    GUEST = "guest"
    STANDARD_USER = "standard_user"
    ADMIN = "admin"


@dataclass
class UserContext:
    user_id: str
    role: UserRole


class SensitivityLevel(Enum):
    LOW = "LOW"         # Bebas dieksekusi tanpa konfirmasi
    MEDIUM = "MEDIUM"   # Perlu role STANDARD_USER ke atas
    HIGH = "HIGH"       # Perlu role ADMIN + Persetujuan Human-in-the-Loop (HITL)


class ToolRegistry:
    """Registri tool yang dilengkapi permissioning RBAC dan HITL Gate."""

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, name: str, sensitivity: SensitivityLevel, required_roles: List[UserRole], func: Callable):
        self.tools[name] = {
            "sensitivity": sensitivity,
            "required_roles": required_roles,
            "func": func
        }

    def execute_tool(self, tool_name: str, user: UserContext, hitl_approved: bool = False, **kwargs) -> str:
        if tool_name not in self.tools:
            return f"{RED}[ERROR]: Tool '{tool_name}' tidak ditemukan.{RESET}"

        tool_meta = self.tools[tool_name]
        sensitivity = tool_meta["sensitivity"]
        required_roles = tool_meta["required_roles"]

        # Check 1: Role-Based Access Control (RBAC)
        if user.role not in required_roles:
            return (
                f"{RED}[ACCESS DENIED - RBAC]: User '{user.user_id}' (Role: {user.role.value}) "
                f"tidak memiliki izin untuk memanggil tool '{tool_name}'. "
                f"Peran yang dibutuhkan: {[r.value for r in required_roles]}{RESET}"
            )

        # Check 2: Human-in-the-Loop (HITL) Gate untuk High Sensitivity Actions
        if sensitivity == SensitivityLevel.HIGH and not hitl_approved:
            return (
                f"{YELLOW}[HITL GATE TRIGGERED]: Tool '{tool_name}' tergolong HIGH SENSITIVITY. "
                f"Eksekusi DITAHAN menunggu konfirmasi persetujuan manusia (Human Approval)!{RESET}"
            )

        # Eksekusi Tool jika lolos semua verifikasi
        result = tool_meta["func"](**kwargs)
        return f"{GREEN}[SUCCESS]: {result}{RESET}"


# --- Contoh Tool Functions ---
def read_system_status() -> str:
    return "Status Sistem: Semua server berjalan normal (Uptime 99.9%)."

def update_user_profile(user_id: str, new_name: str) -> str:
    return f"Profil pengguna {user_id} diperbarui menjadi '{new_name}'."

def delete_database_records(table_name: str) -> str:
    return f"Tabel '{table_name}' telah DIHAPUS PERMANEN dari database."


def main():
    print(f"\n{BOLD}{CYAN}=== DEMO 2.1: TOOL PERMISSION & RBAC (WITH HITL GATE) ==={RESET}\n")

    registry = ToolRegistry()
    registry.register_tool("read_status", SensitivityLevel.LOW, [UserRole.GUEST, UserRole.STANDARD_USER, UserRole.ADMIN], read_system_status)
    registry.register_tool("update_profile", SensitivityLevel.MEDIUM, [UserRole.STANDARD_USER, UserRole.ADMIN], update_user_profile)
    registry.register_tool("delete_db", SensitivityLevel.HIGH, [UserRole.ADMIN], delete_database_records)

    guest_user = UserContext(user_id="usr_guest01", role=UserRole.GUEST)
    std_user = UserContext(user_id="usr_john", role=UserRole.STANDARD_USER)
    admin_user = UserContext(user_id="admin_boss", role=UserRole.ADMIN)

    # 1. Guest mencoba panggil tool LOW vs HIGH
    print(f"{BOLD}[1] UJI COBA AKSES USER ROLE: GUEST{RESET}")
    print(f"-> Guest memanggil 'read_status':")
    print(registry.execute_tool("read_status", guest_user))
    print(f"-> Guest memanggil 'delete_db':")
    print(registry.execute_tool("delete_db", guest_user))
    print()

    # 2. Standard User mencoba panggil update_profile vs delete_db
    print(f"{BOLD}[2] UJI COBA AKSES USER ROLE: STANDARD USER{RESET}")
    print(f"-> Standard User memanggil 'update_profile':")
    print(registry.execute_tool("update_profile", std_user, user_id="usr_john", new_name="John Doe"))
    print(f"-> Standard User memanggil 'delete_db':")
    print(registry.execute_tool("delete_db", std_user))
    print()

    # 3. Admin mencoba panggil delete_db tanpa vs dengan HITL approval
    print(f"{BOLD}[3] UJI COBA AKSES USER ROLE: ADMIN (DENGAN HITL GATE){RESET}")
    print(f"-> Admin memanggil 'delete_db' TANPA persetujuan HITL:")
    print(registry.execute_tool("delete_db", admin_user, hitl_approved=False, table_name="audit_logs"))
    print(f"-> Admin memanggil 'delete_db' DENGAN persetujuan HITL (Approved by Operator):")
    print(registry.execute_tool("delete_db", admin_user, hitl_approved=True, table_name="audit_logs"))
    print()

    print(f"{BOLD}{GREEN}✔ Simulasi Modul 2.1 Selesai.{RESET}\n")


if __name__ == "__main__":
    main()
