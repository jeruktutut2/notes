from prepare_data import siapkan_dataset_jsonl
from fine_tune import buat_ollama_modelfile, cetak_template_unsloth_qlora

if __name__ == "__main__":
    print("=========================================================")
    print("CHATBOT INTERAKTIF: FINE TUNING (MODUL 8)")
    print("=========================================================")
    
    while True:
        print("\nPilih Skenario Fine Tuning:")
        print("1. Siapkan Dataset JSONL")
        print("2. Buat Ollama Modelfile & Tampilkan Template QLoRA")
        pilihan = input("Pilihan (1/2) atau 'keluar': ").strip()

        if pilihan.lower() in ['keluar', 'exit', 'q']:
            print("Sampai jumpa!")
            break
            
        if pilihan not in ['1', '2']:
            print("Pilihan tidak valid.")
            continue
            
        if pilihan == '1':
            siapkan_dataset_jsonl()
        elif pilihan == '2':
            buat_ollama_modelfile()
            cetak_template_unsloth_qlora()
            
        print("\n" + "-"*50)
