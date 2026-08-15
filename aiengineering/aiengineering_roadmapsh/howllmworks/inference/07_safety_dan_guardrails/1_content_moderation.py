"""
=================================================================
1. CONTENT MODERATION
=================================================================
Content moderation = memfilter konten yang tidak pantas, berbahaya,
atau melanggar kebijakan sebelum dikirim ke user.

Layer moderation:
1. INPUT moderation  → Cek prompt user sebelum dikirim ke model
2. OUTPUT moderation → Cek response model sebelum dikirim ke user
3. Both (recommended) → Cek keduanya

Kategori konten yang dimoderasi:
- Hate speech / ujaran kebencian
- Violence / kekerasan
- Sexual content / konten seksual
- Self-harm / melukai diri sendiri
- Illegal activities / aktivitas ilegal
- PII (Personal Identifiable Information)
=================================================================
"""

import re
from dataclasses import dataclass


@dataclass
class ModerationResult:
    """Hasil moderasi konten."""
    is_flagged: bool
    categories: dict  # kategori: True/False
    scores: dict      # kategori: skor (0-1)
    action: str       # "allow", "warn", "block"


class SimpleContentModerator:
    """
    Content moderator sederhana menggunakan keyword matching.
    
    ⚠️ CATATAN: Di production, gunakan API moderasi profesional:
    - OpenAI Moderation API (gratis!)
    - Perspective API (Google)
    - Azure Content Safety
    - AWS Comprehend
    """

    def __init__(self):
        # Daftar kata/frasa yang dilarang (contoh sederhana)
        self.blocked_patterns = {
            "violence": [
                r"\b(kill|murder|attack|bomb|weapon|hurt someone)\b",
            ],
            "hate_speech": [
                r"\b(hate\s+(all|every)\s+\w+)\b",
                r"\b(inferior|subhuman)\b",
            ],
            "pii": [
                r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",  # Phone number (US)
                r"\b\d{16}\b",                         # Credit card
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",  # Email
                r"\b\d{3}-\d{2}-\d{4}\b",              # SSN
            ],
            "self_harm": [
                r"\b(suicide|self[- ]harm)\b",
            ],
        }

        # Threshold untuk setiap kategori
        self.thresholds = {
            "violence": 0.5,
            "hate_speech": 0.5,
            "pii": 0.3,  # Lebih sensitif untuk PII
            "self_harm": 0.3,
        }

    def moderate(self, text: str) -> ModerationResult:
        """Moderasi sebuah teks."""
        text_lower = text.lower()
        categories = {}
        scores = {}

        for category, patterns in self.blocked_patterns.items():
            matches = 0
            for pattern in patterns:
                found = re.findall(pattern, text_lower, re.IGNORECASE)
                matches += len(found)

            # Skor sederhana berdasarkan jumlah match
            score = min(matches / max(len(patterns), 1), 1.0)
            categories[category] = score >= self.thresholds[category]
            scores[category] = round(score, 3)

        is_flagged = any(categories.values())
        
        # Tentukan aksi
        if any(categories.get(cat) for cat in ["violence", "hate_speech", "self_harm"]):
            action = "block"
        elif categories.get("pii"):
            action = "warn"
        else:
            action = "allow"

        return ModerationResult(
            is_flagged=is_flagged,
            categories=categories,
            scores=scores,
            action=action
        )


def demo_content_moderation():
    """Demo content moderation."""
    print("=" * 60)
    print("DEMO 1: Content Moderation")
    print("=" * 60)

    moderator = SimpleContentModerator()

    teks_list = [
        ("Aman", "How do I make a chocolate cake?"),
        ("Aman", "What is the capital of Indonesia?"),
        ("PII", "My email is john@example.com and phone is 555-123-4567"),
        ("Violence", "How to make a weapon to attack someone"),
        ("Hate", "I hate all people from that inferior group"),
    ]

    print(f"\n📊 Hasil Moderasi:")
    print(f"   {'Label':<10} | {'Flagged':>7} | {'Action':<6} | Teks")
    print(f"   {'-'*10}-+-{'-'*7}-+-{'-'*6}-+-{'-'*40}")

    for label, teks in teks_list:
        result = moderator.moderate(teks)
        flag = "🚫 Ya" if result.is_flagged else "✅ Tdk"
        action_emoji = {"allow": "✅", "warn": "⚠️", "block": "🛑"}
        print(f"   {label:<10} | {flag:>7} | {action_emoji[result.action]} {result.action:<5} | {teks[:45]}")

        if result.is_flagged:
            flagged_cats = [k for k, v in result.categories.items() if v]
            print(f"   {'':>10}   → Kategori: {', '.join(flagged_cats)}")


def demo_openai_moderation():
    """Contoh penggunaan OpenAI Moderation API."""
    print("\n" + "=" * 60)
    print("DEMO 2: OpenAI Moderation API (Production-Ready)")
    print("=" * 60)

    print("""
    💡 OpenAI menyediakan Moderation API GRATIS — bahkan tanpa
       berlangganan GPT-4. Sangat direkomendasikan untuk production.

    📝 Contoh Penggunaan:

    ```python
    from openai import OpenAI
    client = OpenAI()

    # Moderasi input user
    response = client.moderations.create(
        model="omni-moderation-latest",
        input="Teks yang ingin dimoderasi"
    )

    result = response.results[0]

    if result.flagged:
        print("⚠️ Konten terdeteksi bermasalah!")
        
        # Cek kategori spesifik
        categories = result.categories
        print(f"Hate: {categories.hate}")
        print(f"Violence: {categories.violence}")
        print(f"Sexual: {categories.sexual}")
        print(f"Self-harm: {categories.self_harm}")
        
        # Skor per kategori (0-1)
        scores = result.category_scores
        print(f"Hate score: {scores.hate:.4f}")
    else:
        print("✅ Konten aman, lanjutkan ke model")
    ```

    📋 Kategori yang Dicek:
    ┌─────────────────────┬──────────────────────────────┐
    │ Kategori            │ Deskripsi                    │
    ├─────────────────────┼──────────────────────────────┤
    │ hate                │ Ujaran kebencian             │
    │ hate/threatening    │ Ancaman berbasis kebencian   │
    │ harassment          │ Pelecehan                    │
    │ self-harm           │ Menyakiti diri sendiri       │
    │ sexual              │ Konten seksual               │
    │ sexual/minors       │ Konten seksual anak          │
    │ violence            │ Kekerasan                    │
    │ violence/graphic    │ Kekerasan grafis             │
    │ illicit             │ Aktivitas ilegal             │
    └─────────────────────┴──────────────────────────────┘

    🔄 ALUR MODERATION DI PRODUCTION:
    
    User Input → [INPUT MODERATION] → Model → [OUTPUT MODERATION] → User
                      ↓ (jika flagged)              ↓ (jika flagged)
                  Block/Warn user            Filter output / retry
    """)


def demo_pii_masking():
    """Demo PII (Personal Identifiable Information) masking."""
    print("=" * 60)
    print("DEMO 3: PII Detection & Masking")
    print("=" * 60)

    def mask_pii(text):
        """Mendeteksi dan meng-mask PII dalam teks."""
        masked = text

        # Email
        masked = re.sub(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
            '[EMAIL_MASKED]', masked
        )

        # Phone (berbagai format)
        masked = re.sub(
            r'\b(\+62|62|0)\d{8,12}\b', '[PHONE_MASKED]', masked
        )
        masked = re.sub(
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE_MASKED]', masked
        )

        # Credit card (16 digit)
        masked = re.sub(
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            '[CREDIT_CARD_MASKED]', masked
        )

        # NIK / KTP (16 digit Indonesia)
        masked = re.sub(
            r'\b\d{16}\b', '[NIK_MASKED]', masked
        )

        return masked

    contoh = [
        "Nama saya Budi, email budi@gmail.com, telp 08123456789",
        "Kartu kredit saya 4111 1111 1111 1111 jangan kasih siapa-siapa",
        "Ini nomor KTP saya 3171234567890001 tolong diproses",
        "Cuaca hari ini cerah dan sejuk, cocok untuk jalan-jalan",
    ]

    print(f"\n📊 PII Masking:")
    for teks in contoh:
        masked = mask_pii(teks)
        has_pii = masked != teks
        print(f"\n   Input  : {teks}")
        print(f"   Output : {masked}")
        print(f"   PII?   : {'🔴 Ya (di-mask)' if has_pii else '🟢 Tidak ada PII'}")


def main():
    demo_content_moderation()
    demo_openai_moderation()
    demo_pii_masking()

    print("\n✅ Selesai! Lanjut ke: 2_prompt_injection_defense.py")

if __name__ == "__main__":
    main()
