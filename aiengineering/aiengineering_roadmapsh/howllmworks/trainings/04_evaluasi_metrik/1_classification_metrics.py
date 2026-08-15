from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

def main():
    print("=== 4.1 Evaluasi & Metrik (Klasifikasi) ===\n")
    print("Dalam machine learning, kita harus mengukur seberapa baik model memprediksi data uji.\n")
    
    # Misalkan ini adalah label asli (kebenaran) dari data tes (0 = Kucing, 1 = Anjing)
    y_true = [0, 1, 1, 0, 1, 0, 1, 1]
    
    # Dan ini adalah hasil tebakan dari AI (Model Prediksi)
    # Ada beberapa yang salah tebak
    y_pred = [0, 1, 0, 0, 1, 1, 1, 1]
    
    print(f"Label Asli : {y_true}")
    print(f"Prediksi AI: {y_pred}\n")
    
    # Menghitung Metrik
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    
    print("Hasil Evaluasi:")
    print(f"- Accuracy  (Akurasi keseluruhan)           : {acc:.2f} ({acc*100}%)")
    print(f"- Precision (Akurasi tebakan positif/Anjing): {prec:.2f}")
    print(f"- Recall    (Kemampuan menemukan semua positif): {rec:.2f}")
    print(f"- F1-Score  (Harmonic mean Precision & Recall): {f1:.2f}\n")
    
    print("Laporan Lengkap (Classification Report):")
    # Nama target (0 dan 1 diubah menjadi teks agar mudah dibaca)
    target_names = ['Kucing (0)', 'Anjing (1)']
    print(classification_report(y_true, y_pred, target_names=target_names))

if __name__ == "__main__":
    main()
