from agent_manual import jalankan_agent_manual
from agent_langgraph import jalankan_langgraph_agent_demo
from agent_langgraph_real import jalankan_langgraph_asli

if __name__ == "__main__":
    print("=========================================================")
    print("CHATBOT INTERAKTIF: AGENTIC AI (MODUL 6)")
    print("=========================================================")
    
    while True:
        print("\nPilih Arsitektur Agent:")
        print("1. Agent ReAct Manual (Murni Python/Looping)")
        print("2. Agent LangGraph (Simulasi Stateful Graph)")
        print("3. Agent LangGraph Asli (Real Implementation)")
        pilihan = input("Pilihan (1/2/3) atau 'keluar': ").strip()

        if pilihan.lower() in ['keluar', 'exit', 'q']:
            print("Sampai jumpa!")
            break
            
        if pilihan not in ['1', '2', '3']:
            print("Pilihan tidak valid.")
            continue
            
        tugas = input("\nMasukkan perintah/pertanyaan (Misal: 'cek cuaca' atau 'hitung diskon'): ").strip()
        if tugas.lower() in ['keluar', 'exit', 'q']:
            print("Sampai jumpa!")
            break
        if not tugas:
            continue
            
        if pilihan == '1':
            jalankan_agent_manual(tugas)
        elif pilihan == '2':
            jalankan_langgraph_agent_demo(tugas)
        elif pilihan == '3':
            jalankan_langgraph_asli()
            
        print("\n" + "-"*50)
