#!/usr/bin/env python3
"""
Modul 04: Analyzer Lisensi & Kepatuhan Open Source Model
Memeriksa batasan hukum, hak komersial, dan kepatuhan dari lisensi model
(Apache 2.0, MIT, Llama 3 Community License, RAIL, Commercial Restrictions).
"""

class LicenseChecker:
    LICENSES = {
        "apache-2.0": {
            "name": "Apache License 2.0",
            "type": "Permissive Open Source",
            "commercial_use": True,
            "modification": True,
            "distribution": True,
            "mau_limit": None,
            "patent_grant": True,
            "restrictions": "Wajib melampirkan pemberitahuan hak cipta & lisensi asli."
        },
        "mit": {
            "name": "MIT License",
            "type": "Permissive Open Source",
            "commercial_use": True,
            "modification": True,
            "distribution": True,
            "mau_limit": None,
            "patent_grant": False,
            "restrictions": "Sangat bebas, hanya wajib melampirkan teks lisensi."
        },
        "llama-3.1-community": {
            "name": "Llama 3.1 Community License",
            "type": "Open Weights with Commercial Limit",
            "commercial_use": True,
            "modification": True,
            "distribution": True,
            "mau_limit": "700 Juta Monthly Active Users (MAU)",
            "patent_grant": True,
            "restrictions": "Dilarang menggunakan output Llama 3.1 untuk melatih model kompetitor non-Llama."
        },
        "rail-m": {
            "name": "Responsible AI License (RAIL-M)",
            "type": "Behavioral Restricted Open Weights",
            "commercial_use": True,
            "modification": True,
            "distribution": True,
            "mau_limit": None,
            "patent_grant": False,
            "restrictions": "Melarang penggunaan untuk pengawasan ilegal, disinformasi, dan manipulasi."
        }
    }

    @classmethod
    def analyze_license(cls, license_key: str, active_users: int = 1_000_000) -> dict:
        key = license_key.lower().strip()
        lic = cls.LICENSES.get(key)
        
        if not lic:
            return {"status": "UNKNOWN", "message": f"Lisensi '{license_key}' tidak terdaftar."}
        
        is_compliant = True
        compliance_notes = []

        if lic["mau_limit"] and active_users > 700_000_000:
            is_compliant = False
            compliance_notes.append(f"⚠️ Melebihi batasan MAU ({lic['mau_limit']}). Wajib mengajukan lisensi enterprise khusus Meta.")
        else:
            compliance_notes.append("✅ Penggunaan komersial diizinkan untuk skala pengguna Anda.")

        return {
            "license_name": lic["name"],
            "type": lic["type"],
            "commercial_allowed": lic["commercial_use"],
            "mau_limit": lic["mau_limit"] or "Tanpa Batas",
            "restrictions": lic["restrictions"],
            "is_compliant": is_compliant,
            "notes": compliance_notes
        }

def main():
    print("=" * 75)
    print("      ANALYZER KEPATUHAN LISENSI OPEN SOURCE & OPEN WEIGHTS")
    print("=" * 75)
    
    test_models = [
        {"model": "Mistral-7B-v0.3", "license": "apache-2.0"},
        {"model": "Meta-Llama-3.1-70B", "license": "llama-3.1-community"},
        {"model": "Custom RAIL Model", "license": "rail-m"}
    ]
    
    for item in test_models:
        res = LicenseChecker.analyze_license(item["license"], active_users=5_000_000)
        print(f"\n📦 Model: {item['model']}")
        print(f"   Nama Lisensi   : {res['license_name']} ({res['type']})")
        print(f"   Akses Komersial: {'YA' if res['commercial_allowed'] else 'TIDAK'}")
        print(f"   Batasan MAU    : {res['mau_limit']}")
        print(f"   Klausul Khusus : {res['restrictions']}")
        print(f"   Status Kepatuhan: {res['notes'][0]}")

    print("\n💡 PETUNJUK LEGAL:")
    print("• Selalu verifikasi file `LICENSE` pada direktori repositori model sebelum komersialisasi.")

if __name__ == "__main__":
    main()
