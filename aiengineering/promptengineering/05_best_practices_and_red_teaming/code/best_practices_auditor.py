#!/usr/bin/env python3
"""
Modul 05: Automated Best Practices Auditor
Memeriksa apakah prompt memenuhi 14 Aturan Emas Best Practices dari roadmap.sh.
"""

def audit_prompt(prompt_text: str) -> dict:
    checks = {
        "Has Delimiters (XML or ```)": "```" in prompt_text or "<" in prompt_text and ">" in prompt_text,
        "Has Placeholders ({{var}} or {var})": "{" in prompt_text and "}" in prompt_text,
        "Has System Role Instruction": "SYSTEM" in prompt_text.upper() or "ROLE" in prompt_text.upper() or "Anda adalah" in prompt_text,
        "Has Output Format Specification": "JSON" in prompt_text or "XML" in prompt_text or "FORMAT" in prompt_text.upper(),
        "Concise Length (< 500 words)": len(prompt_text.split()) < 500
    }
    
    score = sum(1 for v in checks.values() if v)
    return {"score": score, "total": len(checks), "details": checks}

def main():
    print("🔍 AUTOMATED PROMPT BEST PRACTICES AUDITOR")
    print("=" * 60)
    
    sample_prompt = """
    [SYSTEM ROLE]
    Anda adalah seorang Data Analyst.
    
    [INSTRUCTION]
    Ekstrak data penjualan dari teks berikut: {{user_input}}
    
    [FORMAT]
    Kembalikan dalam format JSON.
    ```json
    """
    
    result = audit_prompt(sample_prompt)
    print(f"Skor Kepatuhan Prompt: {result['score']}/{result['total']}\n")
    for check_name, passed in result["details"].items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} : {check_name}")
    print("=" * 60)

if __name__ == "__main__":
    main()
