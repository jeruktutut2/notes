import os
import json
from openai import OpenAI

def main():
    print("=== 9.1 Evaluasi Agent (LLM-as-Judge) ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # ---------------------------------------------------------------
    # EVALUASI AGENT
    # Bagaimana mengukur apakah agent menjawab dengan baik?
    #
    # Metode:
    # 1. LLM-as-Judge: Gunakan LLM lain untuk menilai output
    # 2. Reference-based: Bandingkan dengan jawaban referensi
    # 3. Human evaluation: Penilaian manusia (paling akurat, paling mahal)
    # ---------------------------------------------------------------

    # --- METODE 1: LLM-as-Judge ---
    def evaluate_with_llm(question, answer, criteria=None):
        """Menggunakan LLM sebagai penilai (judge) untuk mengevaluasi jawaban."""
        if criteria is None:
            criteria = ["relevansi", "akurasi", "kelengkapan", "kejelasan"]

        criteria_text = "\n".join([f"- {c}" for c in criteria])

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Kamu adalah evaluator AI yang objektif. "
                        "Evaluasi jawaban AI berdasarkan pertanyaan yang diberikan.\n\n"
                        f"Kriteria evaluasi:\n{criteria_text}\n\n"
                        "Berikan penilaian dalam format JSON:\n"
                        "{\n"
                        '  "scores": {"kriteria1": 1-5, "kriteria2": 1-5, ...},\n'
                        '  "overall_score": 1-5,\n'
                        '  "strengths": ["..."],\n'
                        '  "weaknesses": ["..."],\n'
                        '  "verdict": "BAIK/CUKUP/KURANG"\n'
                        "}"
                    )
                },
                {
                    "role": "user",
                    "content": f"Pertanyaan: {question}\n\nJawaban AI: {answer}"
                }
            ],
            temperature=0.0
        )

        result = response.choices[0].message.content.strip()
        try:
            clean = result
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1].rsplit("```", 1)[0]
            return json.loads(clean)
        except:
            return {"error": "Gagal parse", "raw": result}

    # --- METODE 2: Reference-based Evaluation ---
    def evaluate_with_reference(question, answer, reference):
        """Membandingkan jawaban dengan jawaban referensi."""
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Bandingkan jawaban AI dengan jawaban referensi. "
                        "Berikan skor 1-5 untuk kecocokan (1=sangat beda, 5=sangat cocok). "
                        'Kembalikan JSON: {"match_score": 1-5, "missing_info": ["..."], "extra_info": ["..."]}'
                    )
                },
                {
                    "role": "user",
                    "content": f"Pertanyaan: {question}\n\nJawaban AI: {answer}\n\nJawaban Referensi: {reference}"
                }
            ],
            temperature=0.0
        )

        result = response.choices[0].message.content.strip()
        try:
            clean = result
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1].rsplit("```", 1)[0]
            return json.loads(clean)
        except:
            return {"error": "Gagal parse"}

    # --- DEMO: EVALUASI ---
    print("=" * 60)
    print("1. LLM-as-Judge (Evaluasi Tanpa Referensi)")
    print("=" * 60)

    test_cases = [
        {
            "question": "Apa itu AI Agent?",
            "answer": "AI Agent adalah sistem AI yang menggunakan LLM sebagai otak untuk membuat keputusan, berinteraksi dengan tools eksternal seperti API dan database, serta menyelesaikan tugas secara otonom melalui loop berulang (perception → plan → act → observe)."
        },
        {
            "question": "Bagaimana cara membuat nasi goreng?",
            "answer": "Nasi goreng dibuat dari nasi."  # Jawaban terlalu singkat
        },
        {
            "question": "Apa ibukota Jepang?",
            "answer": "Ibukota Jepang adalah Osaka. Osaka terkenal dengan makanan street food-nya."  # Jawaban salah
        },
    ]

    for tc in test_cases:
        print(f"\n{'─'*50}")
        print(f"❓ Q: {tc['question']}")
        print(f"💬 A: {tc['answer']}")

        eval_result = evaluate_with_llm(tc["question"], tc["answer"])

        if "error" not in eval_result:
            print(f"\n📊 Evaluasi:")
            scores = eval_result.get("scores", {})
            for criterion, score in scores.items():
                bar = "█" * score + "░" * (5 - score)
                print(f"   {criterion:<15}: {bar} {score}/5")
            print(f"   {'Overall':<15}: {eval_result.get('overall_score', 'N/A')}/5")
            print(f"   Verdict: {eval_result.get('verdict', 'N/A')}")
            strengths = eval_result.get("strengths", [])
            if strengths:
                print(f"   ✅ Kuat: {', '.join(strengths)}")
            weaknesses = eval_result.get("weaknesses", [])
            if weaknesses:
                print(f"   ⚠️ Lemah: {', '.join(weaknesses)}")
        else:
            print(f"   [Error] {eval_result}")

    # --- METODE 2: Reference-based ---
    print(f"\n{'='*60}")
    print("2. Reference-Based Evaluation (Dengan Jawaban Referensi)")
    print("=" * 60)

    ref_test = {
        "question": "Berapa hari cuti karyawan per tahun?",
        "answer": "Karyawan mendapatkan 12 hari cuti tahunan. Cuti bisa diambil setelah masa percobaan.",
        "reference": "Karyawan berhak atas 12 hari cuti tahunan. Cuti bisa diambil setelah masa percobaan 3 bulan. Cuti yang tidak digunakan bisa diakumulasi maksimal 5 hari ke tahun berikutnya."
    }

    print(f"\n❓ Q: {ref_test['question']}")
    print(f"💬 A: {ref_test['answer']}")
    print(f"📖 R: {ref_test['reference']}")

    ref_eval = evaluate_with_reference(ref_test["question"], ref_test["answer"], ref_test["reference"])
    if "error" not in ref_eval:
        print(f"\n📊 Match Score: {ref_eval.get('match_score', 'N/A')}/5")
        missing = ref_eval.get("missing_info", [])
        if missing:
            print(f"   ❌ Info yang hilang: {', '.join(missing)}")
        extra = ref_eval.get("extra_info", [])
        if extra:
            print(f"   ➕ Info tambahan: {', '.join(extra)}")

    # --- RINGKASAN ---
    print(f"\n{'='*60}")
    print("✅ Selesai! Memahami evaluasi agent.")
    print("\nMetode Evaluasi:")
    print("  1. LLM-as-Judge: LLM menilai output (cepat, scalable)")
    print("  2. Reference-based: Bandingkan dengan golden answer (akurat)")
    print("  3. Human eval: Manusia menilai (paling akurat, paling mahal)")
    print("\nMetrik yang umum:")
    print("  - Relevansi (apakah menjawab pertanyaan)")
    print("  - Akurasi (apakah faktanya benar)")
    print("  - Kelengkapan (apakah informasi lengkap)")
    print("  - Task completion rate (apakah tugas berhasil)")

if __name__ == "__main__":
    main()
