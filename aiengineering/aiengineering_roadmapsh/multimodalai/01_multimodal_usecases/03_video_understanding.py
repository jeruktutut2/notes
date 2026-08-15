"""
03_video_understanding.py
Modul Demonstrasi Video Understanding (Keyframe Sampling, Temporal QA & Action Recognition)
"""

def simulate_keyframe_extraction(video_filename: str, duration_sec: int, fps_sample: float = 0.5) -> list:
    """Mengambil frame penting (keyframes) dari video untuk diproses oleh Vision LLM."""
    print(f"📹 [Video Loader] Memproses '{video_filename}' (Durasi: {duration_sec}s)")
    print(f"✂️ [Sampling Strategy] Uniform Sampling pada rate {fps_sample} Frame Per Second")
    
    keyframes = []
    current_time = 0.0
    frame_idx = 1
    while current_time < duration_sec:
        keyframes.append({
            "frame_id": frame_idx,
            "timestamp": f"{current_time:.1f}s",
            "description": f"Keyframe #{frame_idx} pada detik {current_time:.1f}"
        })
        current_time += (1.0 / fps_sample)
        frame_idx += 1
        
    print(f"📊 Berhasil mengekstraksi {len(keyframes)} keyframes.")
    return keyframes

def simulate_temporal_video_qa(keyframes: list, question: str) -> dict:
    """Melakukan reasoning temporal melintasi deretan keyframes."""
    print(f"\n❓ [Temporal Video QA] Pertanyaan: '{question}'")
    
    # Event tracking simulation across keyframes
    event_timeline = [
        {"time": "0.0s", "event": "Seseorang berjalan mendekati pintu toko."},
        {"time": "4.0s", "event": "Seseorang membuka pintu toko dan melambaikan tangan."},
        {"time": "8.0s", "event": "Seseorang mengambil barang dari rak utama."}
    ]
    
    print("⏳ Menghubungkan konteks temporal (Cross-frame attention):")
    for evt in event_timeline:
        print(f"   • t={evt['time']}: {evt['event']}")
        
    response = (
        "Berdasarkan analisis urutan video (0.0s - 8.0s), subjek pertama kali datang, "
        "membuka pintu pada detik ke-4, dan mengambil barang di rak pada detik ke-8."
    )
    return {
        "question": question,
        "summary": response,
        "detected_actions": ["walking", "opening door", "grabbing item"]
    }

def main():
    print("=" * 70)
    print("🎥 MODUL 03: VIDEO UNDERSTANDING (KEYFRAME SAMPLING & TEMPORAL QA)")
    print("=" * 70)

    # 1. Keyframe extraction
    keyframes = simulate_keyframe_extraction("cctv_store_entrance.mp4", duration_sec=10, fps_sample=0.25)
    for kf in keyframes:
        print(f"  • {kf['description']}")

    # 2. Temporal Video QA
    qa_res = simulate_temporal_video_qa(keyframes, "Jelaskan urutan tindakan orang tersebut dalam video!")
    print(f"\n💡 Summary Hasil Video QA:\n   {qa_res['summary']}")

    print("\n✅ Modul Video Understanding Berhasil Dijalankan!")

if __name__ == "__main__":
    main()
