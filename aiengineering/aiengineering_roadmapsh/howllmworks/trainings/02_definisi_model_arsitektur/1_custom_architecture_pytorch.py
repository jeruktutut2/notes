import torch
import torch.nn as nn

# Mendefinisikan arsitektur jaringan saraf tiruan (Neural Network) secara manual menggunakan PyTorch
class JaringanSederhana(nn.Module):
    def __init__(self):
        super(JaringanSederhana, self).__init__()
        # Layer 1: Input (misal 10 fitur) ke Hidden Layer (20 neuron)
        self.fc1 = nn.Linear(10, 20)
        # Fungsi Aktivasi: ReLU (Rectified Linear Unit) untuk menambahkan non-linearitas
        self.relu = nn.ReLU()
        # Layer 2: Hidden Layer (20 neuron) ke Output Layer (2 kelas, untuk klasifikasi biner)
        self.fc2 = nn.Linear(20, 2)

    def forward(self, x):
        # Alur data (Forward Pass) dari input menuju output
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

def main():
    print("=== 2.1 Mendefinisikan Arsitektur Kustom (PyTorch) ===\n")
    
    # Inisialisasi model yang baru saja kita buat
    model = JaringanSederhana()
    
    print("Struktur Arsitektur Model:")
    print(model)
    
    print("\nSimulasi Forward Pass:")
    # Membuat input dummy/palsu (Batch Size: 5, Fitur: 10)
    input_dummy = torch.randn(5, 10)
    print(f"Ukuran Input: {input_dummy.shape}")
    
    # Memasukkan data ke dalam model
    output = model(input_dummy)
    
    print(f"Ukuran Output: {output.shape} (5 data, 2 prediksi probabilitas kelas)")
    print("Nilai Output (Logits):")
    print(output)

if __name__ == "__main__":
    main()
