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


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

pcs = {}
relay = MediaRelay()
vad = webrtcvad.Vad(2)

@app.get("/")
async def index():
    return HTMLResponse(open("static/index.html").read())

@app.websocket("/ws-vad")
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
            while True:
                try:

                    frame = await track.recv()
                    print(f"frame: {frame}")

                    sample_rate = frame.sample_rate
                    if sample_rate not in [8000, 16000, 32000, 48000]:
                        print(f"Unsupported sample rate: {sample_rate}")
                        # return frame
                    print("Sample rate:", sample_rate)
        
                    # pcm = frame.to_ndarray().tobytes()
                    # sample_rate = frame.sample_rate

                    # Convert to NumPy array (shape: (channels, samples))
                    pcm_array = frame.to_ndarray()
                    print("Channels:", pcm_array.shape[0] if pcm_array.ndim == 2 else 1)
                    print("dtype:", pcm_array.dtype)

                    # Convert to mono if needed (average channels)
                    if pcm_array.ndim == 2:
                        mono_pcm = pcm_array.mean(axis=0).astype(np.int16)
                    else:
                        mono_pcm = pcm_array.astype(np.int16)
        
                    print("PCM max amplitude:", np.max(np.abs(mono_pcm)))
                    print(f"Frame duration: {len(mono_pcm) / sample_rate * 1000:.2f} ms")

                    # Convert to bytes
                    pcm_bytes = mono_pcm.tobytes()

                    # samples = len(pcm) // 2  # 2 bytes per sample
                    # duration_ms = int((samples / sample_rate) * 1000)

                    # if duration_ms in [10, 20, 30] and sample_rate in [8000, 16000, 32000, 48000]:
                    #     is_speech = vad.is_speech(pcm, sample_rate)
                    #     print("Voice Detected" if is_speech else "Silence")
                    # else:
                    #     print(f"Unsupported frame duration/sample_rate: {duration_ms}ms, {sample_rate}Hz")

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
                        is_speech = vad.is_speech(chunk, sample_rate)
                        print("🗣️ Voice Detected" if is_speech else "🔇 Silence")
        
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
                print("offer received")
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


