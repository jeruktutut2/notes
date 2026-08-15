from mcp_client import main as client_main
from mcp_server import main as server_main

if __name__ == "__main__":
    print("=========================================================")
    print("CHATBOT INTERAKTIF: MODEL CONTEXT PROTOCOL (MODUL 10)")
    print("=========================================================")
    
    while True:
        print("\nPilih Skenario MCP:")
        print("1. Jalankan Simulasi MCP Server (Menerima Request)")
        print("2. Jalankan Simulasi MCP Client (Mengirim Request ke Server)")
        pilihan = input("Pilihan (1/2) atau 'keluar': ").strip()

        if pilihan.lower() in ['keluar', 'exit', 'q']:
            print("Sampai jumpa!")
            break
            
        if pilihan not in ['1', '2']:
            print("Pilihan tidak valid.")
            continue
            
        if pilihan == '1':
            print("\n⏳ Menjalankan Simulasi MCP Server...")
            server_main()
        elif pilihan == '2':
            print("\n⏳ Menjalankan Simulasi MCP Client...")
            client_main()
            
        print("\n" + "-"*50)
