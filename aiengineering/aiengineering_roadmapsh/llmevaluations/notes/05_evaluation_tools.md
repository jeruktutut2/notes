# 05. Evaluation Tools: DeepEval & RAGAS

Untuk menerapkan evaluasi skala produksi, pengembang AI menggunakan *framework* khusus yang mempermudah otomatisasi evaluasi, integrasi CI/CD, dan generasi *synthetic dataset*. Dua tools paling populer dan terdepan saat ini adalah **DeepEval** dan **RAGAS**.

---

## 🚀 1. DeepEval (Confident AI)

**DeepEval** adalah kerangka kerja evaluasi LLM open-source berbasis Python yang dirancang dengan filosofi "PyTest for LLMs".

### Fitur Utama DeepEval:
- **Unit Testing Native**: Pengujian LLM seperti *unit test* menggunakan perintah `deepeval test run`.
- **14+ Built-in Metrics**:
  - `GEval`: Metrik kustom dengan CoT.
  - `AnswerRelevancyMetric` & `FaithfulnessMetric`.
  - `HallucinationMetric`.
  - `SummarizationMetric`.
  - `ToxicityMetric` & `BiasMetric`.
- **Synthetic Test Data Generation**: Mampu membangkitkan pasangan *(query, context, gold_standard)* secara otomatis dari dokumen mentah.
- **CI/CD Integration**: Memblokir merge pull request jika skor LLM berada di bawah ambang batas (*threshold*).

### Contoh Sintaksis DeepEval:
```python
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

def test_answer_relevancy():
    test_case = LLMTestCase(
        input="Apa itu RAG?",
        actual_output="RAG adalah Retrieval Augmented Generation yang menggabungkan pencarian dokumen dengan LLM."
    )
    metric = AnswerRelevancyMetric(threshold=0.7)
    assert_test(test_case, [metric])
```

---

## 📊 2. RAGAS (Retrieval Augmented Generation Assessment)

**RAGAS** adalah spesialis framework open-source terpopuler untuk mengevaluasi arsitektur RAG secara end-to-end tanpa memerlukan *ground truth* jawaban ideal buatan manusia.

### Fitur Utama RAGAS:
- **Evaluasi Komponen RAG Terpisah**:
  - **Retriever Evaluation**: *Context Precision*, *Context Recall*, *Context Entities Recall*.
  - **Generator Evaluation**: *Faithfulness*, *Answer Relevance*, *Answer Semantic Similarity*, *Answer Correctness*.
- **Dataset Integration**: Bekerja secara native dengan HuggingFace `datasets` dan LangChain / LlamaIndex integrations.
- **Synthetic Evolution**: Teknik pembuatan test dataset menggunakan *Evolutionary Prompting* (Simple, Reasoning, Multi-context).

### Perbandingan Ringkas DeepEval vs RAGAS:

| Fitur | DeepEval | RAGAS |
| :--- | :--- | :--- |
| **Fokus Utama** | Unit Testing LLM Umum & CI/CD Pipeline | Evaluasi Terintegrasi Pipeline RAG |
| **Ekosistem** | PyTest CLI, Confident AI Platform | LangChain, LlamaIndex, HuggingFace |
| **Generasi Test Set** | Sintetis berbasis Evolusi Documents | Sintetis berbasis Knowledge Graph & Evolution |
| **Metrik Kustom** | Sangat fleksibel via G-Eval API | Dibuat via custom Prompts & RAGAS metrics |
