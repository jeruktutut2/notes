import torch
import torch.nn as nn
import torch.optim as optim

def main():
    print("=== 3.1 Siklus Pelatihan Manual (Training Loop PyTorch) ===\n")
    
    # 1. Persiapan Model, Loss Function, dan Optimizer
    model = nn.Linear(1, 1) # Model regresi linear paling sederhana: y = mx + c
    criterion = nn.MSELoss() # Mean Squared Error (Loss function untuk regresi)
    
    # Optimizer (misal: SGD - Stochastic Gradient Descent) untuk memperbarui bobot
    # lr = 0.01 adalah learning rate (seberapa besar langkah pembaruan bobot)
    optimizer = optim.SGD(model.parameters(), lr=0.01) 
    
    # 2. Persiapan Data Dummy (X = input, Y = target yang diharapkan)
    # Misal rumusnya Y = 2X + 1
    inputs = torch.tensor([[1.0], [2.0], [3.0], [4.0]])
    targets = torch.tensor([[3.0], [5.0], [7.0], [9.0]])
    
    print("Mulai Pelatihan (Training)...\n")
    epochs = 100 # Jumlah putaran pelatihan
    
    for epoch in range(epochs):
        # A. Forward Pass (Prediksi model saat ini)
        outputs = model(inputs)
        
        # B. Menghitung tingkat kesalahan (Loss)
        loss = criterion(outputs, targets)
        
        # C. Kosongkan gradien sebelumnya (wajib di PyTorch sebelum backward pass)
        optimizer.zero_grad()
        
        # D. Backward Pass (Menghitung gradien secara otomatis / Backpropagation)
        loss.backward()
        
        # E. Pembaruan Bobot (Weights Update) oleh Optimizer
        optimizer.step()
        
        # Menampilkan progress setiap 20 epoch
        if (epoch+1) % 20 == 0:
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")
            
    print("\nPelatihan Selesai!")
    
    # Tes prediksi setelah dilatih
    test_input = torch.tensor([[5.0]])
    prediksi = model(test_input)
    print(f"\nUji Coba: X = 5.0")
    print(f"Target yang seharusnya: 11.0 (karena Y = 2(5) + 1)")
    print(f"Prediksi Model: {prediksi.item():.4f}")

if __name__ == "__main__":
    main()
