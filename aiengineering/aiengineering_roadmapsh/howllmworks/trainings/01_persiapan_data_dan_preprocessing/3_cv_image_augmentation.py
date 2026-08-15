# Catatan: Skrip ini membutuhkan library `Pillow`, `torch`, dan `torchvision`.
# Bisa diinstal dengan: pip install Pillow torch torchvision

import os
from PIL import Image, ImageDraw
import torch
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader

def setup_dummy_dataset(base_folder='dataset_images'):
    """Membuat struktur folder dataset gambar dengan beberapa kelas (kucing & anjing)."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_base_folder = os.path.join(base_dir, base_folder)
    
    categories = ['kucing', 'anjing']
    colors = {'kucing': (73, 109, 137), 'anjing': (200, 100, 100)}
    
    os.makedirs(full_base_folder, exist_ok=True)
    
    for category in categories:
        cat_dir = os.path.join(full_base_folder, category)
        os.makedirs(cat_dir, exist_ok=True)
        
        # Buat 2 gambar dummy per kelas (Total 4 gambar)
        for i in range(1, 3):
            img_path = os.path.join(cat_dir, f"{category}_{i}.jpg")
            if not os.path.exists(img_path):
                img = Image.new('RGB', (400, 300), color=colors[category])
                d = ImageDraw.Draw(img)
                d.text((120, 140), f"{category.capitalize()} {i}", fill=(255, 255, 0))
                img.save(img_path)

    return full_base_folder

def main():
    print("=== 3. Pemrosesan Data & Augmentasi Gambar (Multi-Image Batch) ===\n")

    # 1. Menyiapkan folder dataset berisi beberapa gambar
    dataset_dir = setup_dummy_dataset('dataset_images')
    print(f"Menyiapkan folder dataset gambar di: '{dataset_dir}'")
    print("Struktur folder:")
    print("  ├── dataset_images/kucing/ (kucing_1.jpg, kucing_2.jpg)")
    print("  └── dataset_images/anjing/ (anjing_1.jpg, anjing_2.jpg)")

    # 2. Mendefinisikan Pipeline Transformasi & Augmentasi
    transform_pipeline = transforms.Compose([
        transforms.RandomResizedCrop(224),      # Crop & resize acak ke 224x224 (standar ResNet)
        transforms.RandomHorizontalFlip(p=0.5), # Flip horizontal acak (50%)
        transforms.ToTensor(),                  # Ubah PIL Image (0-255) ke PyTorch Tensor (0.0-1.0)
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) # Normalisasi ImageNet
    ])

    print("\nMemuat dataset menggunakan torchvision.datasets.ImageFolder...")
    # Memuat seluruh folder gambar sekaligus
    dataset = ImageFolder(root=dataset_dir, transform=transform_pipeline)
    print(f"Total gambar dalam dataset: {len(dataset)} gambar")
    print(f"Daftar Kelas (Label): {dataset.classes} (Mapping: {dataset.class_to_idx})")

    # 3. Menggunakan DataLoader untuk memproses gambar secara BATCH (sekaligus banyak)
    batch_size = 2
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    print(f"\nMemproses gambar menggunakan DataLoader (Batch Size = {batch_size})...")
    
    for batch_idx, (images, labels) in enumerate(data_loader, 1):
        print(f"\nBatch #{batch_idx}:")
        print(f"  - Shape Tensor Gambar (Batch, Channel, Height, Width): {images.shape}")
        print(f"  - Label Angka Kategori: {labels.tolist()}")

    print("\n" + "=" * 60)
    print("KESIMPULAN:")
    print("Folder Gambar -> Dimuat otomatis oleh ImageFolder ->")
    print("Diaugmentasi & Ditransformasi -> Dikelompokkan ke Batch Tensor oleh DataLoader ->")
    print("SIAP MASUK KE MODEL COMPUTER VISION (ResNet/YOLO/CNN)!")
    print("=" * 60)

if __name__ == "__main__":
    main()
