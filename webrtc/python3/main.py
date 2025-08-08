import asyncio
import json
import uuid
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCConfiguration, RTCIceServer, RTCPeerConnection, RTCIceCandidate
from aiortc.contrib.media import MediaRelay

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Shared resources
pcs = {}
relay = MediaRelay()


@app.get("/")
async def index():
    return HTMLResponse(open("static/index.html").read())


@app.websocket("/webrtc")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    ice_servers = [
        RTCIceServer(urls=["stun:stun.l.google.com:19302"])
    ]
    config = RTCConfiguration(iceServers=ice_servers)
    pc = RTCPeerConnection(configuration=config)
    
    client_id = uuid.uuid4()

    pcs[client_id] = {"pc": pc, "ws": websocket}

    print(f"{client_id} connected")

    # Receive media track
    @pc.on("track")
    async def on_track(track):
        print(f"Track {track.kind} from {client_id}")

        # Find the other peer
        pcs[client_id]["track"] = track
        if len(pcs) > 1:
            for from_pc_id, from_value in pcs.items():
                for to_pc_id, to_value in pcs.items():
                    if from_pc_id != to_pc_id:
                        to_value["pc"].addTrack(from_value["track"])

        # pc.addTrack(track)
        # pc.addTrack(relay.subscribe(track))
    
    pc.addTransceiver("audio")

    @pc.on("icecandidate")
    async def on_ice_candidate(candidate):
        print(f"candidate on_icecandidate: {candidate}")
        candidate_dict = {
            "candidate": candidate.component,  # Sebenarnya yang utama: candidate.to_sdp()
            "sdpMid": candidate.sdpMid,
            "sdpMLineIndex": candidate.sdpMLineIndex,
        } 
        # Kirim via WebSocket (misalnya)
        await websocket.send(json.dumps({
            "type": "ice-candidate",
            "candidate": candidate_dict
        }))

    @pc.on("connectionstatechange")
    async def on_state_change():
        print(f"{client_id} connection state: {pc.connectionState}")

    try:

        # Handle ICE candidates from client
        while True:
            msg = json.loads(await websocket.receive_text())

            if msg["type"] == "offer":
                offer = RTCSessionDescription(sdp=msg["sdp"], type=msg["type"])
                print("offer received")
                await pc.setRemoteDescription(offer)

                # Send answer back
                answer = await pc.createAnswer()
                await pc.setLocalDescription(answer)

                print("send answer")
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
                    # candidate=msg_candidate["candidate"]
                    foundation=cadidate_parts[0].split(":")[1],
                    component=int(cadidate_parts[1]),
                    protocol=cadidate_parts[2],
                    priority=int(cadidate_parts[3]),
                    ip=cadidate_parts[4],
                    port=int(cadidate_parts[5]),
                    type=cadidate_parts[7]
                )
                print("add ice candidate")
                await pc.addIceCandidate(rtc_ice_candidate)

    except Exception as e:
        print("WebSocket closed or error:", e)
    finally:
        await pc.close()
        pcs.pop(client_id, None)
        print(f"{client_id} disconnected")