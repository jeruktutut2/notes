"""
05_building_ai_agents/04_vertex_ai_agent_builder.py
Arsitektur & Simulasi Vertex AI Agent Builder (Google Cloud Enterprise Agent Platform).
"""

import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class VertexAIAgentBuilderSim:
    """Simulasi Arsitektur Vertex AI Agent Builder & Enterprise Grounding."""

    def __init__(self, project_id: str = "my-gcp-enterprise-project", agent_id: str = "hr-policy-agent"):
        self.project_id = project_id
        self.agent_id = agent_id
        self.data_stores = ["gcs-hr-policy-pdf-datastore", "bigquery-employee-db"]
        self.extensions = ["salesforce-api-extension", "sendgrid-email-extension"]

    def show_architecture(self):
        table = Table(title=f"Vertex AI Agent Builder Spec: {self.agent_id}")
        table.add_column("Komponen", style="cyan")
        table.add_column("Deskripsi / Target Integrasi", style="green")

        table.add_row("Google Cloud Project", self.project_id)
        table.add_row("Enterprise Data Stores", ", ".join(self.data_stores))
        table.add_row("API Extensions", ", ".join(self.extensions))
        table.add_row("Grounding Engine", "Google Search Grounding + Enterprise RAG Vector Store")
        table.add_row("Safety & Compliance", "Google Cloud Vertex AI Safety Filters (Active)")

        console.print(table)

    def run_grounded_query(self, user_query: str):
        console.print(Panel(f"[bold yellow]Vertex AI Agent Builder Session[/bold yellow]\nQuery: '{user_query}'", title="Google Cloud Enterprise Agent"))

        # 1. Search Grounding in Data Store
        console.print("\n🔍 [1. Enterprise Grounding]: Mencari dokumen relevan di 'gcs-hr-policy-pdf-datastore'...")
        time.sleep(0.3)
        grounded_citation = {
            "document": "Kebijakan_Cuti_2026.pdf",
            "page": 14,
            "text_snippet": "Karyawan berhak atas cuti tahunan 12 hari setelah masa kerja 1 tahun.",
            "confidence_score": 0.98
        }
        console.print(f"📄 Document Found: [bold]{grounded_citation['document']}[/bold] (Page {grounded_citation['page']})")
        console.print(f"   Snippet: '{grounded_citation['text_snippet']}' (Confidence: {grounded_citation['confidence_score']})")

        # 2. Extension Tool Execution
        console.print("\n⚙️ [2. Executing OpenAPI Extension Tool]: 'bigquery-employee-db.check_employee_tenure'")
        time.sleep(0.2)
        console.print("   Observation: Employee 'Budi' Tenure = 2.5 tahun (Eligible for 12 days leave).")

        # 3. Verified Output Response
        console.print("\n[bold green]✅ Grounded Final Response (Zero Hallucination Guaranteed):[/bold green]")
        console.print("Berdasarkan Dokumen Kebijakan_Cuti_2026.pdf Halaman 14, Anda berhak mengambil cuti tahunan hingga 12 hari per tahun karena masa kerja Anda telah melebihi 1 tahun (2.5 tahun).")

def main():
    agent_sim = VertexAIAgentBuilderSim()
    agent_sim.show_architecture()
    console.print("\n")
    agent_sim.run_grounded_query("Berapa sisa kuota cuti tahunan yang bisa saya ambil tahun ini?")

if __name__ == "__main__":
    main()
