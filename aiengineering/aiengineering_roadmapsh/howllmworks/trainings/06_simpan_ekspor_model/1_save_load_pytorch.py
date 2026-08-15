import torch
import torch.nn as nn
import os

# Definisikan model yang sama dengan yang dilatih
class ModelSederhana(nn.Module):
    def __init__(self):
        super(ModelSederhana, self).__init__()
        self.fc = nn.Linear(5, 2)

    def forward(self, x):
        return self.fc(x)

def main():
    print("=== 6.1 Menyimpan dan Memuat Model PyTorch ===\n")
    
    # 1. Inisialisasi model
    model = ModelSederhana()
    print("Bobot awal sebelum disimpan:")
    print(model.fc.weight)
    
    # Path tempat menyimpan
    save_path = "model_weights.pth"
    
    # 2. MENYIMPAN MODEL (Saving)
    print(f"\nMenyimpan model ke: {save_path} ...")
    # Yang disimpan biasanya hanya state_dict (kumpulan bobot/parameter), bukan seluruh kelas model
    torch.save(model.state_dict(), save_path)
    print("Berhasil disimpan!\n")
    
    # 3. MEMUAT MODEL (Loading)
    # Bayangkan ini di file terpisah atau server produksi
    print("Memuat ulang model (Simulasi di Server Produksi)...")
    model_produksi = ModelSederhana() # Harus mendefinisikan kelasnya lagi
    
    # Memasukkan bobot yang disimpan ke dalam arsitektur kosong
    model_produksi.load_state_dict(torch.load(save_path))
    model_produksi.eval() # Mengubah mode menjadi evaluasi (penting untuk lapisan Dropout/BatchNorm)
    
    print("\nBobot setelah dimuat:")
    print(model_produksi.fc.weight)
    
    # Memeriksa apakah file ada
    if os.path.exists(save_path):
        os.remove(save_path) # Hapus file agar tidak mengotori folder setelah demo
        print("\n(Catatan: File model_weights.pth sementara telah dihapus setelah eksekusi demo ini).")

if __name__ == "__main__":
    main()
