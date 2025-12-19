import json
import uuid
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer, RTCPeerConnection, RTCIceCandidate
from aiortc.contrib.media import MediaRelay
import webrtcvad
from av import AudioFrame
import numpy as np
import asyncio
from faster_whisper import WhisperModel
import librosa
import soundfile as sf

# from fastapi import FastAPI, WebSocket

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

pcs = {}
relay = MediaRelay()
vad = webrtcvad.Vad(2)
silence_counter = 0
frame_duration_ms = 30
silence_threshold_frames = int(1000 / frame_duration_ms)  # 1 detik
# speech_buffer = bytearray()
speech_chunks = []
# model = WhisperModel("tiny", compute_type="int8")
model = WhisperModel("small", device="cpu", compute_type="int8")

@app.get("/")
async def index():
    return HTMLResponse(open("static/index.html").read())

@app.websocket("/speech-to-text")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    ice_servers = [
        RTCIceServer(urls=["stun:stun.l.google.com:19302"])
    ]
    config = RTCConfiguration(iceServers=ice_servers)
    pc = RTCPeerConnection(configuration=config)

    @pc.on("track")
    async def on_track(track):
        print(f"Received {track.kind}")
        async def vad_reader():
            global silence_counter
            # global speech_buffer
            global speech_chunks
            while True:
                try:
                    frame = await track.recv()

                    sample_rate = frame.sample_rate
                    if sample_rate not in [8000, 16000, 32000, 48000]:
                        print(f"Unsupported sample rate: {sample_rate}")
                    # print("Sample rate:", sample_rate)

                    pcm_array = frame.to_ndarray()

                    # Convert to mono if needed (average channels)
                    if pcm_array.ndim == 2:
                        mono_pcm = pcm_array.mean(axis=0).astype(np.int16)
                    else:
                        mono_pcm = pcm_array.astype(np.int16)
                    
                    pcm_bytes = mono_pcm.tobytes()

                    # 30ms chunk = (sample_rate * 30 / 1000) samples
                    bytes_per_sample = 2  # 16-bit
                    samples_per_chunk = int(sample_rate * 30 / 1000)
                    bytes_per_chunk = samples_per_chunk * bytes_per_sample
                    chunks = [
                        pcm_bytes[i:i + bytes_per_chunk]
                        for i in range(0, len(pcm_bytes), bytes_per_chunk)
                        if len(pcm_bytes[i:i + bytes_per_chunk]) == bytes_per_chunk
                    ]

                    # Run VAD on each chunk
                    for chunk in chunks:
                        # pastikan chunk bertipe bytes
                        if not isinstance(chunk, (bytes, bytearray)):
                            # convert safe
                            chunk = bytes(chunk)

                        is_speech = vad.is_speech(chunk, sample_rate)
                        # print("🗣️ Voice Detected" if is_speech else "🔇 Silence")
                        if is_speech:
                            print("🗣️ Voice Detected")
                            silence_counter = 0
                            # speech_buffer.extend(chunk)
                            # speech_buffer.append(chunk)
                            # speech_buffer += chunk 
                            speech_chunks.append(chunk)
                            print("🗣️ Voice Detected, appended chunk len:", len(chunk))
                        else:
                            print("🔇 Silence")
                            silence_counter += 1

                    # debug info
                    print(
                        f"silence_counter: {silence_counter} "
                        f"silence_threshold_frames: {silence_threshold_frames} "
                        f"speech_chunks_count: {len(speech_chunks)} "
                        f"speech_total_bytes: {sum(len(c) for c in speech_chunks)}"
                    )

                    # print(f"silence_counter: {silence_counter} silence_threshold_frames: {silence_threshold_frames} len(speech_buffer): {len(speech_buffer)}")
                    # if silence_counter >= silence_threshold_frames and len(speech_buffer) > 0:
                    if silence_counter >= silence_threshold_frames and speech_chunks:
                        print("Silence terdeteksi selama 1 detik, proses STT...")

                        # gabungkan chunks jadi bytes
                        # (jaga fallback bila elemen ternyata tipe int)
                        first_item = speech_chunks[0]
                        if isinstance(first_item, int):
                            audio_bytes = bytes(speech_chunks)    # unlikely, but safe fallback
                        else:
                            audio_bytes = b"".join(speech_chunks)

                        # Hitung durasi audio dalam detik
                        # audio_duration_sec = len(speech_buffer) / (sample_rate * 2)  # 2 bytes per sample
                        audio_duration_sec = len(audio_bytes) / (sample_rate * 2)  # 2 bytes/sample (int16)
                        print(f"Silence terdeteksi selama 1 detik, proses STT... ({audio_duration_sec:.2f} detik audio)")



                        # Gabungkan buffer
                        # audio_int16 = np.frombuffer(b"".join(speech_buffer), dtype=np.int16)

                        # Konversi ke float32 (-1.0 .. 1.0)
                        # audio_float32 = audio_int16.astype(np.float32) / 32768.0

                        # Resample ke 16 kHz
                        # audio_16k = librosa.resample(audio_float32, orig_sr=48000, target_sr=16000)

                        # dari bytes -> int16 -> float32 -> resample
                        audio_int16 = np.frombuffer(audio_bytes, dtype=np.int16)
                        audio_float32 = audio_int16.astype(np.float32) / 32768.0
                        audio_16k = librosa.resample(audio_float32, orig_sr=sample_rate, target_sr=16000)

                        # Optional: simpan untuk debugging
                        # sf.write("debug.wav", audio_16k, 16000)

                        # Transcribe
                        segments, _ = model.transcribe(audio_16k, language="id")
                        segments = list(segments)

                        if not segments:
                            print("⚠️ Tidak ada teks terdeteksi.")
                        else:
                            for seg in segments:
                                print(f"[STT] {seg.text}")

                            # speech_buffer = bytearray()
                        speech_chunks.clear()
                        silence_counter = 0
                        await asyncio.sleep(60)

                except Exception as e:
                    print("VAD track error:", e)
                    break
        asyncio.ensure_future(vad_reader())

        # pc.addTrack(track)
        pc.addTrack(relay.subscribe(track))
    
    pc.addTransceiver("audio")

    @pc.on("icecandidate")
    async def on_ice_candidate(candidate):
        print(f"candidate on_icecandidate: {candidate}")
        candidate_dict = {
            "candidate": candidate.component,  # Sebenarnya yang utama: candidate.to_sdp()
            "sdpMid": candidate.sdpMid,
            "sdpMLineIndex": candidate.sdpMLineIndex,
        }
        await websocket.send(json.dumps({
            "type": "ice-candidate",
            "candidate": candidate_dict
        }))
    
    @pc.on("connectionstatechange")
    async def on_state_change():
        print(f"connection state: {pc.connectionState}")
    
    try:
        while True:
            msg = json.loads(await websocket.receive_text())
            if msg["type"] == "offer":
                offer = RTCSessionDescription(sdp=msg["sdp"], type=msg["type"])
                await pc.setRemoteDescription(offer)

                answer = await pc.createAnswer()
                await pc.setLocalDescription(answer)

                await websocket.send_text(json.dumps({
                    "type": pc.localDescription.type,
                    "sdp": pc.localDescription.sdp
                }))
            elif msg["type"] == "ice-candidate":
                msg_candidate = msg["candidate"]
                cadidate_parts = msg_candidate["candidate"].split()
                rtc_ice_candidate = RTCIceCandidate(
                    sdpMid=msg_candidate["sdpMid"],
                    sdpMLineIndex=msg_candidate["sdpMLineIndex"],
                    foundation=cadidate_parts[0].split(":")[1],
                    component=int(cadidate_parts[1]),
                    protocol=cadidate_parts[2],
                    priority=int(cadidate_parts[3]),
                    ip=cadidate_parts[4],
                    port=int(cadidate_parts[5]),
                    type=cadidate_parts[7]
                )
                await pc.addIceCandidate(rtc_ice_candidate)
    except Exception as e:
        print("WebSocket closed or error:", e)
    finally:
        await pc.close()

