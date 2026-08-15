"""
01_human_annotation_lab.py
--------------------------
Simulasi Human-in-the-Loop (HITL) Annotation Collector:
1. Pengumpulan Feedback Manusia (Likert 1-5 Scale & Binary Pass/Fail)
2. Fine-Grained Error Categorization (Hallucination, Toxicity, Formatting, Off-topic)
3. Rekapitulasi Statistik & Distribusi Skor Annotator
"""

import json
from datetime import datetime

class HumanAnnotationDataset:
    def __init__(self):
        self.annotations = []

    def record_annotation(self, 
                          sample_id: str, 
                          user_prompt: str, 
                          llm_output: str, 
                          annotator_id: str, 
                          likert_score: int, 
                          passed: bool, 
                          error_tags: list[str] = None, 
                          notes: str = "") -> dict:
        """Merekam satu entri penilaian dari annotator manusia."""
        if not (1 <= likert_score <= 5):
            raise ValueError("Skala Likert harus berada antara 1 hingga 5.")

        entry = {
            "sample_id": sample_id,
            "user_prompt": user_prompt,
            "llm_output": llm_output,
            "annotator_id": annotator_id,
            "likert_score": likert_score,
            "passed": passed,
            "error_tags": error_tags or [],
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        self.annotations.append(entry)
        return entry

    def get_summary_statistics(self) -> dict:
        """Menghitung agregasi statistik dari data annotator."""
        if not self.annotations:
            return {"total_annotations": 0}

        scores = [a["likert_score"] for a in self.annotations]
        passes = [1 if a["passed"] else 0 for a in self.annotations]
        
        all_tags = []
        for a in self.annotations:
            all_tags.extend(a["error_tags"])

        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

        return {
            "total_annotations": len(self.annotations),
            "average_likert_score": round(sum(scores) / len(scores), 2),
            "pass_rate_percentage": round((sum(passes) / len(passes)) * 100, 1),
            "error_distribution": tag_counts
        }


if __name__ == "__main__":
    print("=== LAB 07: HUMAN ANNOTATION & FEEDBACK COLLECTOR ===")

    dataset = HumanAnnotationDataset()

    # Simulated Annotation Submissions from Annotator 1 & 2
    dataset.record_annotation(
        sample_id="SAMPLE-01",
        user_prompt="Sebutkan 3 kota terbesar di Indonesia.",
        llm_output="1. Jakarta 2. Surabaya 3. Bandung",
        annotator_id="Annotator_Alice",
        likert_score=5,
        passed=True,
        error_tags=[],
        notes="Sangat akurat."
    )

    dataset.record_annotation(
        sample_id="SAMPLE-02",
        user_prompt="Berapa hasil 15 * 14?",
        llm_output="Hasilnya adalah 220.", # Should be 210
        annotator_id="Annotator_Bob",
        likert_score=2,
        passed=False,
        error_tags=["hallucination", "math_error"],
        notes="Perhitungan salah. 15*14=210."
    )

    dataset.record_annotation(
        sample_id="SAMPLE-03",
        user_prompt="Tuliskan script python hello world",
        llm_output="Sure! Here is the python code: print('Hello World')",
        annotator_id="Annotator_Alice",
        likert_score=4,
        passed=True,
        error_tags=["formatting_issue"],
        notes="Kode berfungsi namun tidak dalam markdown codeblock."
    )

    stats = dataset.get_summary_statistics()

    print(f"\n[Total Annotations Recorded]: {stats['total_annotations']}")
    print(f"[Average Likert Score (1-5)] : ⭐ {stats['average_likert_score']} / 5.0")
    print(f"[Human Pass Rate]            : {stats['pass_rate_percentage']}%")
    print(f"[Error Tag Distribution]     : {stats['error_distribution']}")
