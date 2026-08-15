import optuna

# Fungsi objektif yang ingin kita optimalkan (mencari nilai minimum)
# Dalam AI, fungsi objektif biasanya adalah fungsi yang menjalankan proses training
# dan mengembalikan nilai Loss atau Akurasi dari validation set.
def objective(trial):
    # 1. Mendefinisikan hyperparameter yang ingin dicoba secara otomatis
    # Misal kita ingin mencari nilai 'x' terbaik di antara -10 hingga 10
    x = trial.suggest_float("x", -10, 10)
    
    # Misal kita ingin mencoba berbagai Learning Rate (log scale)
    lr = trial.suggest_float("learning_rate", 1e-5, 1e-1, log=True)
    
    # 2. Rumus matematis (sebagai simulasi dari 'Loss Function' Neural Network)
    # Kita buat rumus parabola: (x - 2)^2. Nilai minimumnya pasti di x = 2.
    # Kita tambahkan elemen lr agar simulasi lebih realistis.
    loss = (x - 2)**2 + (lr * 0.1)
    
    return loss

def main():
    print("=== 5.1 Hyperparameter Tuning dengan Optuna ===\n")
    print("Optuna akan mencoba berbagai kombinasi nilai 'x' dan 'learning_rate'")
    print("secara cerdas untuk mencari nilai 'Loss' terendah.\n")
    
    # Membuat sebuah "study" untuk meminimalkan nilai fungsi objektif
    study = optuna.create_study(direction="minimize")
    
    # Menjalankan proses pencarian sebanyak 50 kali percobaan (trials)
    # n_trials dikurangi agar tidak terlalu lama di terminal
    study.optimize(objective, n_trials=30)
    
    print("\nPencarian Selesai!")
    
    # Mendapatkan hasil terbaik
    best_trial = study.best_trial
    
    print(f"\nLoss Terbaik  : {best_trial.value:.4f}")
    print("Hyperparameter Terbaik yang ditemukan:")
    for key, value in best_trial.params.items():
        print(f"- {key}: {value}")
        
    print("\nCatatan: Dalam skenario nyata (AI), nilai 'x' bisa berupa Batch Size, Dropout Rate, dll.")

if __name__ == "__main__":
    main()
