#!/usr/bin/env python3
"""
main.py
-------
Interactive CLI Runner untuk Modul Pembelajaran Model Context Protocol (MCP).
Menyajikan menu untuk menjalankan skrip-skrip komponen inti dan praktik pengembangan MCP.
"""

import sys
import os
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("\033[95m" + "="*60 + "\033[0m")
    print("\033[93m🚀 MODEL CONTEXT PROTOCOL (MCP) - LEARNING WORKSPACE\033[0m")
    print("\033[95m" + "="*60 + "\033[0m")
    print("Modul Pembelajaran Interaktif berdasarkan AI Engineer Roadmap & Architecture")
    print()

def main_menu():
    while True:
        print_header()
        print("\033[96m--- 📍 CORE COMPONENTS --- \033[0m")
        print(" [1] Run MCP Host & Client Lifecycle (01_core_components/mcp_host_client.py)")
        print(" [2] Run Server Data Primitives Demo (01_core_components/mcp_server_primitives.py)")
        print(" [3] Run Transports Comparison Demo (01_core_components/mcp_transports.py)")
        print()
        print("\033[96m--- 🛠️ DEVELOPING WITH MCP --- \033[0m")
        print(" [4] Run Building an MCP Server Demo (02_developing_with_mcp/building_mcp_server.py)")
        print(" [5] Run Building an MCP Client Demo (02_developing_with_mcp/building_mcp_client.py)")
        print(" [6] Run Connect to Local Server Demo (02_developing_with_mcp/connect_local_server.py)")
        print(" [7] Run Connect to Remote Server Demo (02_developing_with_mcp/connect_remote_server.py)")
        print()
        print("\033[96m--- 🌐 OTHER OPTIONS --- \033[0m")
        print(" [8] Run ALL Demos Sequentially")
        print(" [9] Start Web Visualizer HTTP Server (Port 8000)")
        print(" [0] Exit")
        print()

        choice = input("\033[92mPilih Menu [0-9]: \033[0m").strip()

        if choice == "1":
            subprocess.run([sys.executable, "01_core_components/mcp_host_client.py"])
        elif choice == "2":
            subprocess.run([sys.executable, "01_core_components/mcp_server_primitives.py"])
        elif choice == "3":
            subprocess.run([sys.executable, "01_core_components/mcp_transports.py"])
        elif choice == "4":
            subprocess.run([sys.executable, "02_developing_with_mcp/building_mcp_server.py"])
        elif choice == "5":
            subprocess.run([sys.executable, "02_developing_with_mcp/building_mcp_client.py"])
        elif choice == "6":
            subprocess.run([sys.executable, "02_developing_with_mcp/connect_local_server.py"])
        elif choice == "7":
            subprocess.run([sys.executable, "02_developing_with_mcp/connect_remote_server.py"])
        elif choice == "8":
            scripts = [
                "01_core_components/mcp_host_client.py",
                "01_core_components/mcp_server_primitives.py",
                "01_core_components/mcp_transports.py",
                "02_developing_with_mcp/building_mcp_server.py",
                "02_developing_with_mcp/building_mcp_client.py",
                "02_developing_with_mcp/connect_local_server.py",
                "02_developing_with_mcp/connect_remote_server.py"
            ]
            for s in scripts:
                print(f"\n\033[94m>>> RUNNING {s} <<<\033[0m")
                subprocess.run([sys.executable, s])
                print("-" * 50)
        elif choice == "9":
            print("\n🌐 Membuka Web Visualizer Server pada http://localhost:8000")
            print("Tekan Ctrl+C untuk menghentikan server.")
            try:
                subprocess.run([sys.executable, "-m", "http.server", "8000", "--directory", "web_visualizer"])
            except KeyboardInterrupt:
                print("\nServer dihentikan.")
        elif choice == "0":
            print("Terima kasih! Selamat belajar MCP.")
            break
        else:
            print("Pilihan tidak valid, tekan Enter untuk mencoba lagi...")
        
        input("\nTekan [ENTER] untuk melanjutkan...")
        clear_screen()

if __name__ == "__main__":
    main_menu()
