"""
01_image_understanding.py
Modul Demonstrasi Image Understanding (Visual Question Answering, OCR & Object Detection)
"""

import base64
import json

def generate_mock_image_bytes() -> bytes:
    """Membuat mock pixel data PNG 1x1 sederhana sebagai bytes."""
    # Base64 1x1 red PNG
    b64_str = "iVBORw0KGgoAAAANSU5CYII="
    return base64.b64decode(b64_str)

def format_image_to_base64_payload(image_bytes: bytes, mime_type: str = "image/png") -> str:
    """Mengubah raw bytes gambar ke format Data URL Base64 yang siap dikirim ke Vision API."""
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

def simulate_visual_qa(image_description: str, question: str) -> dict:
    """Simulasi pengolahan Visual Question Answering (VQA) oleh Vision LLM."""
    print(f"🖼️ [VQA Input] Gambar: '{image_description}'")
    print(f"❓ [VQA Question] Pertanyaan: '{question}'")
    
    # Visual reasoning logic simulation
    reasoning_steps = [
        "1. Ekstraksi fitur visual (Patch Extraction via Vision Encoder).",
        "2. Proyeksi visual embedding ke dimensi LLM space (Linear Projection Layer).",
        "3. Cross-attention antara instruksi teks & fitur gambar.",
        "4. Generasi jawaban kontekstual berbasis objek yang terdeteksi."
    ]
    
    answer = f"Berdasarkan visual '{image_description}', ditemukan objek terkait '{question}' dengan estimasi kepastian 98.4%."
    return {
        "question": question,
        "reasoning": reasoning_steps,
        "answer": answer
    }

def simulate_ocr_and_layout_analysis() -> dict:
    """Simulasi OCR (Optical Character Recognition) dan ekstraksi dokumen terstruktur."""
    print("\n📜 [OCR Engine] Menganalisis Dokumen Struk Transaksi...")
    detected_blocks = [
        {"text": "TOKO SERBA ADA", "bbox": [50, 20, 250, 50], "confidence": 0.99},
        {"text": "Item: Kopi Susu Gula Aren", "bbox": [30, 80, 280, 100], "confidence": 0.97},
        {"text": "Harga: Rp 25.000", "bbox": [30, 110, 200, 130], "confidence": 0.98},
        {"text": "Total: Rp 25.000", "bbox": [30, 150, 200, 170], "confidence": 0.99}
    ]
    return {
        "status": "SUCCESS",
        "blocks_count": len(detected_blocks),
        "extracted_data": detected_blocks
    }

def main():
    print("=" * 70)
    print("👁️ MODUL 01: IMAGE UNDERSTANDING (VQA, OCR & OBJECT DETECTION)")
    print("=" * 70)

    # 1. Base64 Encoding
    img_bytes = generate_mock_image_bytes()
    b64_payload = format_image_to_base64_payload(img_bytes)
    print(f"\n1. Data URL Base64 Payload Header: {b64_payload[:45]}...")

    # 2. Visual Question Answering Simulation
    print("\n2. Visual Question Answering (VQA) Simulation:")
    vqa_result = simulate_visual_qa(
        image_description="Foto papan petunjuk arah bandara di Terminal 3",
        question="Di mana posisi gate penerbangan internasional?"
    )
    for step in vqa_result["reasoning"]:
        print(f"   {step}")
    print(f"💡 Jawaban LLM: {vqa_result['answer']}")

    # 3. OCR Simulation
    print("\n3. OCR & Document Layout Extraction:")
    ocr_result = simulate_ocr_and_layout_analysis()
    print(json.dumps(ocr_result, indent=2, ensure_ascii=False))

    print("\n✅ Modul Image Understanding Berhasil Dijalankan!")

if __name__ == "__main__":
    main()
