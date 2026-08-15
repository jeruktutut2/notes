import uvicorn
import requests
import json

def jalankan_server():
    print("\n⏳ Menjalankan FastAPI Server di port 8000...")
    print("Buka browser di: http://localhost:8000/docs")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)

def test_klien_api():
    print("\n--- TEST KLIEN API CHAT ---")
    while True:
        prompt = input("Kamu: ").strip()
        if prompt.lower() in ['keluar', 'exit', 'q']:
            break
        if not prompt:
            continue
            
        try:
            res = requests.post(
                "http://localhost:8000/v1/chat",
                json={"prompt": prompt, "system_prompt": "Kamu asisten yang ramah.", "temperature": 0.7}
            )
            if res.status_code == 200:
                data = res.json()
                print(f"AI (Cache: {data['cached']} | {data['latency_sec']}s): {data['response']}")
            else:
                print("Error dari server:", res.text)
        except requests.exceptions.ConnectionError:
            print("❌ Gagal terhubung ke server API. Pastikan server dijalankan dulu di tab terpisah.")
            
if __name__ == "__main__":
    print("=========================================================")
    print("CHATBOT INTERAKTIF & SERVER API: DEPLOYMENT (MODUL 11)")
    print("=========================================================")
    
    while True:
        print("\nPilih Mode:")
        print("1. Jalankan Production REST API Server (FastAPI)")
        print("2. Coba Chat (Sebagai Klien API)")
        pilihan = input("Pilihan (1/2) atau 'keluar': ").strip()

        if pilihan.lower() in ['keluar', 'exit', 'q']:
            print("Sampai jumpa!")
            break
            
        if pilihan not in ['1', '2']:
            print("Pilihan tidak valid.")
            continue
            
        if pilihan == '1':
            jalankan_server()
            break # Uvicorn will block
        elif pilihan == '2':
            test_klien_api()
            
        print("\n" + "-"*50)
