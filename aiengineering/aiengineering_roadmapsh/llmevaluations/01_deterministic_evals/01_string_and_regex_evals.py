"""
01_string_and_regex_evals.py
----------------------------
Demonstrasi Evaluasi Deterministik berbasis:
1. Exact Match & Case-Insensitive String Match
2. Levenshtein Distance & Similarity Ratio
3. Substring / Keyword Presence Check
4. Regex Extraction & Structural Validation
"""

import re

def exact_match(prediction: str, target: str, ignore_case: bool = True, strip_whitespace: bool = True) -> bool:
    """Menguji apakah dua string persis sama."""
    if strip_whitespace:
        prediction = prediction.strip()
        target = target.strip()
    if ignore_case:
        prediction = prediction.lower()
        target = target.lower()
    return prediction == target

def levenshtein_distance(str1: str, str2: str) -> int:
    """Menhitung jumlah langkah edit (insert, delete, substitute) dari str1 ke str2."""
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]

def levenshtein_similarity(str1: str, str2: str) -> float:
    """Menghitung nisbah kemiripan Levenshtein (0.0 hingga 1.0)."""
    max_len = max(len(str1), len(str2))
    if max_len == 0:
        return 1.0
    dist = levenshtein_distance(str1, str2)
    return round(1.0 - (dist / max_len), 4)

def keyword_coverage(text: str, required_keywords: list[str]) -> dict:
    """Memeriksa persentase kata kunci wajib yang muncul di luaran."""
    text_lower = text.lower()
    found = [kw for kw in required_keywords if kw.lower() in text_lower]
    missing = [kw for kw in required_keywords if kw.lower() not in text_lower]
    coverage = len(found) / len(required_keywords) if required_keywords else 1.0
    return {
        "coverage_score": round(coverage, 2),
        "found_keywords": found,
        "missing_keywords": missing,
        "passed": coverage == 1.0
    }

def validate_regex_format(text: str, pattern: str) -> dict:
    """Validasi teks menggunakan pola Regex tertentu."""
    match = re.search(pattern, text)
    return {
        "pattern": pattern,
        "is_valid": match is not None,
        "extracted_match": match.group(0) if match else None
    }

if __name__ == "__main__":
    print("=== LAB 01: STRING & REGEX DETERMINISTIC EVALS ===")
    
    # 1. Exact Match Test
    pred = "   Jakarta is the capital of Indonesia.  "
    target = "jakarta is the capital of indonesia."
    em = exact_match(pred, target)
    print(f"\n[1] Exact Match Test:")
    print(f"    Pred  : '{pred.strip()}'")
    print(f"    Target: '{target.strip()}'")
    print(f"    Result: {'PASSED (Match)' if em else 'FAILED'}")

    # 2. Levenshtein Distance & Similarity
    s1 = "Artificial Intelligence"
    s2 = "Artificail Inteligence"
    dist = levenshtein_distance(s1, s2)
    sim = levenshtein_similarity(s1, s2)
    print(f"\n[2] Levenshtein Similarity:")
    print(f"    String 1: '{s1}'")
    print(f"    String 2: '{s2}'")
    print(f"    Distance: {dist} edits")
    print(f"    Similarity Score: {sim * 100:.1f}%")

    # 3. Keyword Coverage
    sample_response = "Sistem RAG menggunakan Vector Database untuk mencari context relevan dan memberikannya ke LLM."
    keywords = ["RAG", "Vector Database", "LLM", "Embedding", "Reranker"]
    cov = keyword_coverage(sample_response, keywords)
    print(f"\n[3] Keyword Coverage Check:")
    print(f"    Required Keywords: {keywords}")
    print(f"    Coverage Score: {cov['coverage_score'] * 100:.0f}%")
    print(f"    Found Keywords   : {cov['found_keywords']}")
    print(f"    Missing Keywords : {cov['missing_keywords']}")

    # 4. Regex Pattern Validation (Email extraction test)
    email_sample = "Hubungi support kami di admin@aiengineering.id untuk info lebih lanjut."
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    res = validate_regex_format(email_sample, email_pattern)
    print(f"\n[4] Regex Email Validation:")
    print(f"    Sample Text: '{email_sample}'")
    print(f"    Valid Email Found: {res['is_valid']}")
    print(f"    Extracted Email  : {res['extracted_match']}")
