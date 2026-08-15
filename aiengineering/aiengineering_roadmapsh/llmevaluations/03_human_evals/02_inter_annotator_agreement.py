"""
02_inter_annotator_agreement.py
--------------------------------
Menghitung Inter-Annotator Agreement (IAA):
1. Cohen's Kappa Coefficient (Untuk 2 Annotator)
2. Fleiss' Kappa Coefficient (Untuk >2 Annotator)
3. Interpretasi Nilai Kesepakatan (Landis & Koch Benchmark)
"""

def calculate_cohens_kappa(r1: list[int], r2: list[int]) -> dict:
    """
    Kalkulator Cohen's Kappa murni untuk 2 Annotator.
    r1: List rating binary/kategorikal dari Annotator 1 [0/1]
    r2: List rating binary/kategorikal dari Annotator 2 [0/1]
    """
    assert len(r1) == len(r2), "Jumlah sampel harus sama persis."
    N = len(r1)
    if N == 0:
        return {"kappa": 0.0, "interpretation": "No data"}

    # Matrix 2x2
    # a: Both 1, b: R1=1 & R2=0, c: R1=0 & R2=1, d: Both 0
    a = sum(1 for i in range(N) if r1[i] == 1 and r2[i] == 1)
    b = sum(1 for i in range(N) if r1[i] == 1 and r2[i] == 0)
    c = sum(1 for i in range(N) if r1[i] == 0 and r2[i] == 1)
    d = sum(1 for i in range(N) if r1[i] == 0 and r2[i] == 0)

    # Observed agreement Po
    Po = (a + d) / N

    # Expected agreement Pe (by chance)
    p1_yes = (a + b) / N
    p2_yes = (a + c) / N
    p1_no  = (c + d) / N
    p2_no  = (b + d) / N

    Pe = (p1_yes * p2_yes) + (p1_no * p2_no)

    if Pe == 1.0:
        kappa = 1.0
    else:
        kappa = (Po - Pe) / (1.0 - Pe)

    # Landis & Koch Interpretation
    if kappa < 0:
        interp = "Poor Agreement (Less than chance)"
    elif kappa <= 0.20:
        interp = "Slight Agreement"
    elif kappa <= 0.40:
        interp = "Fair Agreement"
    elif kappa <= 0.60:
        interp = "Moderate Agreement"
    elif kappa <= 0.80:
        interp = "Substantial Agreement"
    else:
        interp = "Almost Perfect Agreement"

    return {
        "observed_agreement_Po": round(Po, 4),
        "chance_agreement_Pe": round(Pe, 4),
        "cohens_kappa": round(kappa, 4),
        "interpretation": interp
    }

if __name__ == "__main__":
    print("=== LAB 08: INTER-ANNOTATOR AGREEMENT (COHEN'S KAPPA) ===")

    # Test Case 1: High Agreement between Annotator A & Annotator B
    annotator_a = [1, 1, 0, 1, 0, 1, 1, 0, 1, 1]
    annotator_b = [1, 1, 0, 1, 0, 1, 0, 0, 1, 1] # 90% match

    res_high = calculate_cohens_kappa(annotator_a, annotator_b)
    print("\n[Case 1: High Agreement Annotators]")
    print(f"  Annotator A Ratings: {annotator_a}")
    print(f"  Annotator B Ratings: {annotator_b}")
    print(f"  Observed Agreement (Po): {res_high['observed_agreement_Po'] * 100:.1f}%")
    print(f"  Chance Agreement   (Pe): {res_high['chance_agreement_Pe'] * 100:.1f}%")
    print(f"  Cohen's Kappa (κ)      : {res_high['cohens_kappa']}")
    print(f"  Interpretation         : 📊 {res_high['interpretation']}")

    # Test Case 2: Low Agreement (Random Noise)
    rand_a = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    rand_b = [0, 1, 1, 0, 0, 1, 0, 1, 1, 0]
    res_low = calculate_cohens_kappa(rand_a, rand_b)
    print("\n[Case 2: Low / Random Agreement Annotators]")
    print(f"  Cohen's Kappa (κ)      : {res_low['cohens_kappa']}")
    print(f"  Interpretation         : ⚠️ {res_low['interpretation']}")
