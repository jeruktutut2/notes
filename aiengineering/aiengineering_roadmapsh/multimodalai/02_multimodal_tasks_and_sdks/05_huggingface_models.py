"""
05_huggingface_models.py
Modul Task & SDK: Hugging Face Models (CLIP Visual-Text Alignment, BLIP Captioning & Florence-2)
"""

import math

def simulate_clip_similarity_score(image_label: str, text_candidates: list) -> list:
    """Simulasi kalkulasi Cosine Similarity antara Image Embedding & Text Embedding menggunakan CLIP (Contrastive Language-Image Pre-training)."""
    print(f"🖼️ [CLIP Model] Target Gambar: '{image_label}'")
    print(f"🔤 [CLIP Text Encoder] Menghitung dot product similarity dengan candidate labels...")
    
    # Simulated cosine similarity scores
    scores = [
        {"text": "A photo of a Golden Retriever dog playing in the park", "score": 0.942},
        {"text": "A sports car driving on a highway", "score": 0.041},
        {"text": "A plate of delicious gourmet pasta", "score": 0.017}
    ]
    return scores

def simulate_blip_image_captioning(image_label: str) -> str:
    """Simulasi generasi deskripsi teks (Captioning) menggunakan BLIP / BLIP-2."""
    print(f"\n📝 [BLIP Model Pipeline] Generasi caption otomatis untuk '{image_label}'...")
    caption = "a golden retriever dog sitting happily in the green grass on a sunny day"
    return caption

def simulate_florence2_multitask(task_prompt: str) -> dict:
    """Simulasi model vision multi-task Microsoft Florence-2."""
    print(f"\n⚡ [Florence-2 Pipeline] Running Task Prompt: '{task_prompt}'")
    
    if "<OD>" in task_prompt:  # Object Detection
        return {
            "task": "Object Detection",
            "bboxes": [
                {"label": "dog", "box": [120, 80, 450, 510]},
                {"label": "frisbee", "box": [300, 210, 380, 290]}
            ]
        }
    else:  # Dense Captioning
        return {
            "task": "Dense Captioning",
            "captions": [
                "a golden retriever with a yellow collar",
                "a green plastic frisbee on the grass"
            ]
        }

def main():
    print("=" * 70)
    print("🤗 MODUL SDK 05: HUGGING FACE MULTIMODAL MODELS (CLIP, BLIP, FLORENCE-2)")
    print("=" * 70)

    # 1. CLIP Zero-Shot Classification
    print("\n1. CLIP Zero-Shot Classification:")
    clip_res = simulate_clip_similarity_score("dog_park.jpg", ["dog in park", "sports car", "pasta"])
    for cand in clip_res:
        print(f"   • Label: '{cand['text']}' -> Score: {cand['score']*100:.1f}%")

    # 2. BLIP Captioning
    print("\n2. BLIP Image Captioning:")
    caption = simulate_blip_image_captioning("dog_park.jpg")
    print(f"   💡 Generated Caption: \"{caption}\"")

    # 3. Florence-2 Multi-Task Vision
    print("\n3. Florence-2 Multi-Task Vision:")
    od_res = simulate_florence2_multitask("<OD>")
    print(f"   Detected Objects (<OD>): {od_res['bboxes']}")

    print("\n✅ Modul Hugging Face Models Berhasil Dijalankan!")

if __name__ == "__main__":
    main()
