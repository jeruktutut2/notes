#!/usr/bin/env python3
"""
Modul 04: Evaluation, Testing, Debugging & Monitoring - Part 2
Simulasi Debugging, Structured Logging, Tracing & Observabilitas:
- Structured Logging & Spans (Trace ID & Span ID generation)
- Observability Payload Formatting:
  - LangSmith Runs
  - Helicone Proxy Telemetry Headers
  - LangFuse Trace Schema
  - OpenLLMetry (OpenTelemetry Standard)
"""

import json
import time
import uuid
from typing import Dict, Any

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"


# ============================================================================
# 1. STRUCTURED LOGGING & TRACING ENGINE
# ============================================================================
class StructuredLogger:
    """Mesin Logging Terstruktur berbasis OpenTelemetry Spans."""

    def __init__(self, service_name: str = "agent-architecture-service"):
        self.service_name = service_name
        self.trace_id = f"trc-{uuid.uuid4().hex[:12]}"

    def log_span(self, span_name: str, parent_span_id: str = None, attributes: Dict[str, Any] = None) -> Dict[str, Any]:
        span_id = f"spn-{uuid.uuid4().hex[:8]}"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        span_log = {
            "timestamp": timestamp,
            "service": self.service_name,
            "trace_id": self.trace_id,
            "span_id": span_id,
            "parent_span_id": parent_span_id,
            "name": span_name,
            "attributes": attributes or {}
        }
        return span_log


# ============================================================================
# 2. OBSERVABILITY PAYLOAD FORMATTERS
# ============================================================================
def demo_observability_formatters():
    logger = StructuredLogger()
    print(f"\n{BOLD}{CYAN}=== STRUCTURED LOGGING & TRACING SPAN LOGS ==={RESET}")

    # Root Agent Run Span
    root_span = logger.log_span("AgentRun: ReActLoop", attributes={"user_id": "usr_99", "model": "gpt-4o"})
    print(f"Root Span Created: {BLUE}{json.dumps(root_span, indent=2)}{RESET}")

    # Child Tool Execution Span
    tool_span = logger.log_span(
        "ToolInvocation: SearchDB", 
        parent_span_id=root_span["span_id"],
        attributes={"tool_name": "search_db", "latency_ms": 142, "status_code": 200}
    )
    print(f"\nChild Span Created: {GREEN}{json.dumps(tool_span, indent=2)}{RESET}")

    print(f"\n{BOLD}{MAGENTA}=== OBSERVABILITY INTEGRATIONS OVERVIEW ==={RESET}")

    # LangSmith Payload
    langsmith_run = {
        "name": "PlannerAgentExecutor",
        "run_type": "chain",
        "inputs": {"question": "Analisis stok"},
        "outputs": {"answer": "Stok OK"},
        "extra": {"metadata": {"environment": "production"}}
    }
    print(f"1. {YELLOW}[LangSmith Run Payload]:{RESET}\n{json.dumps(langsmith_run, indent=2)}")

    # Helicone Headers
    helicone_headers = {
        "Helicone-Auth": "Bearer sk-helicone-xxx",
        "Helicone-Property-User": "enterprise_user_12",
        "Helicone-Cache-Enabled": "true"
    }
    print(f"\n2. {YELLOW}[Helicone Proxy Headers]:{RESET}\n{json.dumps(helicone_headers, indent=2)}")

    # LangFuse Trace
    langfuse_trace = {
        "id": logger.trace_id,
        "name": "agent_architecture_flow",
        "userId": "user_42",
        "metadata": {"sdk_version": "2.4.1"}
    }
    print(f"\n3. {YELLOW}[LangFuse Trace Schema]:{RESET}\n{json.dumps(langfuse_trace, indent=2)}")

    # OpenLLMetry Standard
    print(f"\n4. {YELLOW}[OpenLLMetry / OpenTelemetry Standard]:{RESET}")
    print("   • Standardized spans for LLM Provider API Calls, Vector DB queries, and Tool Execution.")


def main():
    print(f"{BOLD}{GREEN}===================================================={RESET}")
    print(f"{BOLD}{GREEN} MODUL 04.2: DEBUGGING & MONITORING FOR AGENTS      {RESET}")
    print(f"{BOLD}{GREEN}===================================================={RESET}")

    demo_observability_formatters()


if __name__ == "__main__":
    main()
