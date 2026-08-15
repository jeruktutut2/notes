"""
01_agents_usecases/demo_usecases.py
Simulasi Kasus Penggunaan (Use Cases) AI Agents dalam Dunia Nyata.
Dapat dijalankan secara mandiri tanpa API Key external (menggunakan mock LLM & simulated tools).
"""

import time
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

console = Console()

class CustomerSupportAgentDemo:
    """Simulasi AI Agent untuk Layanan Pelanggan (Automated Ticket & Refund)"""
    def __init__(self):
        self.orders_db = {
            "ORD-9901": {"status": "DELIVERED", "amount": 250000, "item": "Keyboard Mekanikal", "eligible_refund": True},
            "ORD-9902": {"status": "SHIPPED", "amount": 500000, "item": "Headset Wireless", "eligible_refund": False}
        }

    def check_order_status(self, order_id: str) -> str:
        order = self.orders_db.get(order_id)
        if not order:
            return f"Error: Order ID {order_id} tidak ditemukan."
        return f"Order {order_id}: Item={order['item']}, Status={order['status']}, RefundEligible={order['eligible_refund']}"

    def process_refund(self, order_id: str) -> str:
        order = self.orders_db.get(order_id)
        if not order:
            return f"Error: Order {order_id} tidak valid."
        if not order['eligible_refund']:
            return f"Gagal Refund: Order {order_id} masih dalam pengiriman (SHIPPED)."
        return f"SUKSES: Refund sebesar Rp {order['amount']:,} untuk order {order_id} telah diproses ke saldo pelanggan."

    def run(self, user_request: str, order_id: str):
        console.print(Panel(f"[bold cyan]Skenario 1: Customer Support Agent[/bold cyan]\nUser Request: '{user_request}'", title="Agent Use Case 1"))
        
        # Step 1: Goal Evaluation
        console.print("[yellow][THOUGHT 1][/yellow] User meminta refund. Saya harus memeriksa status pesanan terlebih dahulu.")
        time.sleep(0.3)
        
        # Step 2: Action Check Status
        console.print(f"[cyan][ACTION 1][/cyan] Memanggil Tool: check_order_status('{order_id}')")
        obs1 = self.check_order_status(order_id)
        console.print(f"[green][OBSERVATION 1][/green] {obs1}")
        time.sleep(0.3)

        # Step 3: Thought 2
        console.print("[yellow][THOUGHT 2][/yellow] Pesanan ditemukan dan memenuhi syarat refund. Saya akan memproses refund sekarang.")
        time.sleep(0.3)

        # Step 4: Action Refund
        console.print(f"[cyan][ACTION 2][/cyan] Memanggil Tool: process_refund('{order_id}')")
        obs2 = self.process_refund(order_id)
        console.print(f"[green][OBSERVATION 2][/green] {obs2}")
        time.sleep(0.3)

        # Step 5: Final Answer
        console.print("[bold green][FINAL ANSWER][/bold green] Halo! Refund Anda sebesar Rp 250.000 untuk pesanan #ORD-9901 telah berhasil diproses. Saldo akan masuk dalam 1-3 hari kerja.")


def print_usecase_overview():
    tree = Tree("[bold gold1]Peta Usecases AI Agents dalam Industri[/bold gold1]")
    
    cs = tree.add("🎧 1. Customer Support & E-commerce")
    cs.add("Otomasikan Refund & Pengembalian Barang")
    cs.add("Verifikasi Identitas & Escalation Tiket")
    
    dev = tree.add("💻 2. Software Engineering Assistants")
    dev.add("Autonomous Bug Detection & Fixing")
    dev.add("Refactoring & Test Case Generation")
    
    data = tree.add("📊 3. Research & Data Analysis")
    data.add("Web Crawling & Data Extraction")
    data.add("Automated Chart & Report Generation")

    enterprise = tree.add("🏢 4. Enterprise Workflow Automation")
    enterprise.add("Sync HubSpot CRM <-> Slack <-> Jira")
    enterprise.add("Automated Invoice Auditing")

    console.print(tree)

def main():
    print_usecase_overview()
    console.print("\n")
    agent = CustomerSupportAgentDemo()
    agent.run("Saya mau minta refund untuk pesanan ORD-9901 karena barangnya cacat.", "ORD-9901")

if __name__ == "__main__":
    main()
