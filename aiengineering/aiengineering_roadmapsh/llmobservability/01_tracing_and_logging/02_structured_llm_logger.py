"""
02_structured_llm_logger.py
---------------------------
Lab runnable untuk mendemonstrasikan Structured OpenInference JSON Logging
terhadap pasangan Prompt-Completion, Metadata, dan Token Usage.
"""

import json
import time
import datetime

class OpenInferenceLogger:
    """Standardized OpenInference LLM JSON Logger"""
    
    def __init__(self, service_name: str = "ai-support-service"):
        self.service_name = service_name

    def log_llm_call(
        self,
        trace_id: str,
        model_name: str,
        messages: list,
        response_text: str,
        prompt_tokens: int,
        completion_tokens: int,
        latency_ms: float,
        user_id: str = "anonymous",
        metadata: dict = None
    ) -> str:
        
        record = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "service.name": self.service_name,
            "trace_id": trace_id,
            "attributes": {
                "openinference.span.kind": "LLM",
                "llm.model_name": model_name,
                "llm.input_messages": messages,
                "llm.output_messages": [{"role": "assistant", "content": response_text}],
                "llm.token_count.prompt": prompt_tokens,
                "llm.token_count.completion": completion_tokens,
                "llm.token_count.total": prompt_tokens + completion_tokens,
                "llm.latency_ms": latency_ms,
                "user.id": user_id,
                "custom.metadata": metadata or {}
            }
        }
        
        return json.dumps(record, indent=2)


def main():
    print(f"\n=======================================================")
    print(f"📊 STRUCTURED OPENINFERENCE LOGGING LAB")
    print(f"=======================================================\n")

    logger = OpenInferenceLogger(service_name="customer-copilot-api")

    # Sample conversation messages
    sample_messages = [
        {"role": "system", "content": "You are an assistant for an online electronics store."},
        {"role": "user", "content": "Bagaimana cara melakukan retur barang yang rusak?"}
    ]

    sample_response = (
        "Untuk melakukan retur barang yang rusak, ikuti langkah berikut:\n"
        "1. Buka menu Pesanan Saya di aplikasi.\n"
        "2. Pilih produk yang rusak lalu klik 'Ajukan Komplain'.\n"
        "3. Unggah foto/video unboxing dan pilih opsi Retur/Refund."
    )

    print("Mengirim sampel log LLM call ke format OpenInference JSON...\n")

    log_output = logger.log_llm_call(
        trace_id="tr-88391a0b",
        model_name="gpt-4o",
        messages=sample_messages,
        response_text=sample_response,
        prompt_tokens=42,
        completion_tokens=58,
        latency_ms=480.5,
        user_id="usr_5521",
        metadata={"environment": "production", "feature_flag": "enable_v2_prompt"}
    )

    print(log_output)
    print("\n✅ Log terstruktur berhasil dicetak! Log format ini siap untuk dikirim ke Elasticsearch, Datadog, atau Vector/FluentBit.")

if __name__ == "__main__":
    main()
