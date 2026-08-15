import os
import subprocess

if __name__ == "__main__":
    print("=========================================================")
    print("CHATBOT INTERAKTIF: EVALUASI AI (MODUL 7)")
    print("=========================================================")
    
    while True:
        print("\nPilih Skenario Evaluasi:")
        print("1. Jalankan Semua Evaluasi (Pytest)")
        print("2. LLM-as-a-Judge (Evaluasi kalimat Anda)")
        pilihan = input("Pilihan (1/2) atau 'keluar': ").strip()

        if pilihan.lower() in ['keluar', 'exit', 'q']:
            print("Sampai jumpa!")
            break
            
        if pilihan not in ['1', '2']:
            print("Pilihan tidak valid.")
            continue
            
        if pilihan == '1':
            print("\n⏳ Menjalankan Pytest...")
            subprocess.run(["pytest", "test_ai.py", "-v", "-s"])
        elif pilihan == '2':
            tugas = input("\nMasukkan kalimat penjelasan singkat untuk dinilai (Misal: 'Air mendidih pada suhu 100 derajat celcius'): ").strip()
            if not tugas:
                continue
            
            from test_ai import panggil_ai, json
            
            prompt_judge = f"""Kamu adalah Evaluator Kualitas Konten Edukasi.
Tugasmu adalah menilai jawaban berikut berdasarkan 2 kriteria:
1. Keakuratan fakta ilmiah.
2. Kejelasan untuk anak usia Sekolah Dasar (SD).

Jawaban yang Dinilai: {tugas}

Berikan skor antara 1 sampai 5 (di mana 5 sangat bagus) dalam format JSON murni:
{{"skor": 5, "alasan": "Penjelasan sangat jernih dan mudah dipahami."}}
"""
            print("\n⏳ Menilai dengan LLM-as-a-Judge...")
            try:
                raw_judge_res = panggil_ai(prompt_judge, format_json=True, temperature=0.0)
                data_judge = json.loads(raw_judge_res)
                print(f"👩‍⚖️ Skor: {data_judge.get('skor', 0)}/5")
                print(f"Alasan: {data_judge.get('alasan', '')}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
        print("\n" + "-"*50)
