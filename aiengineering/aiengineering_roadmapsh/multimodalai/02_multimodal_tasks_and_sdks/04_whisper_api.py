"""
04_whisper_api.py
Modul Task & SDK: Whisper API (Audio Transcription, Translation & Format Exports)
"""

import json

def simulate_whisper_api_transcribe(file_path: str, model: str = "whisper-1", language: str = "id", response_format: str = "verbose_json") -> dict:
    """Simulasi pemanggilan API OpenAI Whisper untuk Transkripsi Audio."""
    print(f"📡 [Whisper API Request] Endpoint: https://api.openai.com/v1/audio/transcriptions")
    print(f"🎙️ Audio File: '{file_path}' | Model: {model} | Language: {language}")
    
    mock_verbose_response = {
        "task": "transcribe",
        "language": "indonesian",
        "duration": 12.45,
        "text": "Selamat datang di pembelajaran Whisper API. Sistem ini mampu mengonversi suara menjadi teks secara akurat.",
        "segments": [
            {
                "id": 0,
                "seek": 0,
                "start": 0.0,
                "end": 4.5,
                "text": " Selamat datang di pembelajaran Whisper API.",
                "tokens": [50364, 3421, 8812, 1021, 50589],
                "temperature": 0.0,
                "avg_logprob": -0.15,
                "compression_ratio": 1.2,
                "no_speech_prob": 0.01
            },
            {
                "id": 1,
                "seek": 450,
                "start": 4.5,
                "end": 12.45,
                "text": " Sistem ini mampu mengonversi suara menjadi teks secara akurat.",
                "tokens": [50589, 4412, 1102, 9912, 51021],
                "temperature": 0.0,
                "avg_logprob": -0.12,
                "compression_ratio": 1.3,
                "no_speech_prob": 0.005
            }
        ]
    }
    return mock_verbose_response

def simulate_whisper_api_translation(file_path: str) -> dict:
    """Simulasi pemanggilan API OpenAI Whisper untuk Penerjemahan Otomatis ke Bahasa Inggris."""
    print(f"\n🌐 [Whisper API Translation] Endpoint: https://api.openai.com/v1/audio/translations")
    print(f"🎙️ Audio File (Bahasa Asal: Apapun) -> Output Language: English")
    
    return {
        "text": "Welcome to the Whisper API tutorial. This system accurately converts speech to text."
    }

def main():
    print("=" * 70)
    print("🎙️ MODUL SDK 04: OPENAI WHISPER AUDIO TRANSCRIPTION API")
    print("=" * 70)

    # 1. Transcription
    print("\n1. Panggilan API Transkripsi Audio (verbose_json):")
    trans_res = simulate_whisper_api_transcribe("interview_audio_id.mp3", response_format="verbose_json")
    print(f"📝 Full Transcribed Text:\n   \"{trans_res['text']}\"")
    print("\n   Detailed Segments:")
    for seg in trans_res["segments"]:
        print(f"   • [{seg['start']}s -> {seg['end']}s] {seg['text'].strip()}")

    # 2. Translation
    print("\n2. Panggilan API Penerjemahan Otomatis ke English:")
    transl_res = simulate_whisper_api_translation("interview_audio_id.mp3")
    print(f"💡 Translated Result:\n   \"{transl_res['text']}\"")

    print("\n✅ Modul Whisper API Berhasil Dijalankan!")

if __name__ == "__main__":
    main()
