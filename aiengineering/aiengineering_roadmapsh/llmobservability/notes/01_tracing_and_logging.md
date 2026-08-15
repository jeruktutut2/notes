# 01 - Tracing & Logging dalam LLM Observability

## Overview
Dalam aplikasi berbasis Large Language Model (LLM), tracing dan logging bukan sekadar mencatat teks stdout/stderr biasa. Karena LLM bersifat non-deterministik, multi-step (seperti RAG, Agentic chains, tool calling), dan memiliki biaya per token, **LLM Tracing & Logging** membutuhkan pelacakan hierarkis yang mendalam atas setiap langkah eksekusi.

---

## 1. Konsep Utama: Trace, Span, dan Event

Observability pada LLM mengadopsi standar **OpenTelemetry** dan **OpenInference**:

```
[Trace ID: tr-9842a] (Keseluruhan eksekusi permintaan user)
 ├── [Span: Agent Pipeline] (Parent Span)
 │    ├── [Span: User Query Preprocessing] (Child Span)
 │    ├── [Span: Vector DB Retrieval] (Child Span - Chroma/Pinecone)
 │    │    └── Event: Found 4 relevant document chunks
 │    ├── [Span: Prompt Construction] (Child Span - Context Injection)
 │    └── [Span: LLM Inference - gpt-4o] (Child Span)
 │         ├── Event: Prompt Tokens: 1,420
 │         ├── Event: Completion Tokens: 280
 │         └── Event: Time to First Token (TTFT): 340ms
```

### Definisi Komponen:
1. **Trace**: Mewakili satu workflow atau permintaan pengguna dari awal hingga akhir. Mengandung ID unik (`trace_id`).
2. **Span**: Mewakili satu unit kerja spesifik dalam Trace (misal: panggil LLM, query database, format prompt). Mengandung `span_id`, `parent_span_id`, `start_time`, `end_time`, dan metadata.
3. **Event / Annotation**: Kejadian poin-in-waktu di dalam Span (misal: pencatatan event streaming token pertama).

---

## 2. Standard Metadata yang Wajib Dicatat (OpenInference)

Agar log LLM dapat dianalisis oleh platform observability standar, metadata berikut disarankan:

| Field Name | Deskripsi | Contoh |
|------------|-----------|--------|
| `llm.model_name` | Nama model yang dipanggil | `gpt-4o`, `claude-3-5-sonnet` |
| `llm.prompt_template` | Template prompt sebelum variabel diisi | `"Jawab pertanyaan {query} berdasarkan {context}"` |
| `llm.input_messages` | Daftar pesan input (Role + Content) | `[{"role": "user", "content": "..."}]` |
| `llm.output_messages` | Hasil respons dari LLM | `[{"role": "assistant", "content": "..."}]` |
| `llm.token_count.prompt` | Jumlah token input | `1250` |
| `llm.token_count.completion` | Jumlah token output | `310` |
| `llm.token_count.total` | Total token | `1560` |
| `llm.temperature` | Nilai temperatur model | `0.7` |
| `llm.latency_ms` | Total durasi eksekusi LLM | `850` |

---

## 3. Implementasi Custom Span Tracer dalam Python

Contoh dasar implementasi context manager untuk Span tracing:

```python
import time
import uuid

class Span:
    def __init__(self, name, parent_id=None):
        self.span_id = str(uuid.uuid4())[:8]
        self.parent_id = parent_id
        self.name = name
        self.metadata = {}
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        self.duration_ms = round((self.end_time - self.start_time) * 1000, 2)

    def set_attribute(self, key, value):
        self.metadata[key] = value
```

---

## 4. Keuntungan Tracing & Logging untuk AI Engineer

1. **Debugging Multi-step Agent**: Melacak langkah spesifik mana yang gagal saat Agent mengalami loop atau salah memilih Tool.
2. **Auditability & Compliance**: Menyimpan histori prompt & completion untuk kepatuhan regulasi dan audit keamanan.
3. **Data Replay**: Menggunakan log input/output historis untuk membuat dataset evaluasi fine-tuning dan benchmark.
