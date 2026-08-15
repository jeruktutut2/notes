# 04. Tools & Frameworks for AI Regression Testing 🧰🚀

Berikut adalah lanskap alat (*tooling ecosystem*) populer yang digunakan oleh tim AI Engineering untuk menjalankan pengujian regresi LLM & RAG:

---

## 1. Promptfoo
**Promptfoo** adalah CLI tool dan library open-source populer untuk evaluasi prompt dan pengujian regresi LLM.
- **Fitur Utama**: Matrix testing (menguji N prompt $\times$ M model $\times$ K test cases), CI/CD integration, visual web UI viewer, out-of-the-box red teaming & safety assertions.
- **Penggunaan**:
  ```bash
  npx promptfoo@latest eval
  npx promptfoo@latest view
  ```

---

## 2. DeepEval (Confident AI)
**DeepEval** adalah framework testing Python untuk LLM yang terintegrasi secara mulus dengan `pytest`.
- **Fitur Utama**: G-Eval (custom LLM metrics), Hallucination metric, Answer Relevancy, Summarization metric, Synthetic dataset generator.
- **Penggunaan**:
  ```python
  from deepeval import assert_test
  from deepeval.metrics import AnswerRelevancyMetric
  from deepeval.test_case import LLMTestCase

  def test_answer_relevancy():
      metric = AnswerRelevancyMetric(threshold=0.7)
      test_case = LLMTestCase(input="Apa ibu kota Indonesia?", actual_output="Ibu kota Indonesia adalah Jakarta.")
      assert_test(test_case, [metric])
  ```

---

## 3. Ragas (Retrieval Augmented Generation Assessment)
**Ragas** ditujukan khusus untuk mengukur regresi pada pipeline RAG.
- **Metrik Utama**: Context Precision, Context Recall, Faithfulness, Answer Semantic Similarity.
- **Penggunaan**: Mengukur apakah pembaruan database vektor atau model embedding menyebabkan penurunan daya temu dokumen (*recall*) atau kenaikan halusinasi.

---

## 4. Pytest & Custom Python Test Harness
Untuk proyek yang membutuhkan fleksibilitas penuh tanpa mengikat ke SaaS tertentu, membangun harness pengujian regresi berbasis `pytest` dengan modul `pydantic` dan `scikit-learn` / `numpy` adalah solusi terbaik, tangguh, dan dapat berjalan di server lokal maupun CI/CD runner.
