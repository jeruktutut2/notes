<script setup>
let pc
let isCaller = false

const start = async (caller) => {
  isCaller = caller
  pc = new RTCPeerConnection({
    iceServers: [
      { urls: "stun:localhost:3478" }, // Ganti sesuai STUN/TURN kamu
    ]
  })

  pc.ontrack = (event) => {
    const audio = new Audio()
    audio.srcObject = event.streams[0]
    audio.autoplay = true
  }

  pc.onicecandidate = (event) => {
    if (event.candidate) {
      fetch(`/${isCaller ? "caller-candidate" : "callee-candidate"}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ candidate: event.candidate })
      })
    }
  }

  const stream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false })
  stream.getTracks().forEach(track => pc.addTrack(track, stream))

  if (caller) {
    const offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    await fetch("/offer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sdp: offer })
    })

    const res = await fetch("/answer")
    const data = await res.json()
    await pc.setRemoteDescription(new RTCSessionDescription(data.sdp))
  } else {
    const res = await fetch("/offer")
    const data = await res.json()
    await pc.setRemoteDescription(new RTCSessionDescription(data.sdp))

    const answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    await fetch("/answer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sdp: answer })
    })
  }

  setInterval(async () => {
    const res = await fetch(`/${isCaller ? "callee-candidate" : "caller-candidate"}`)
    const data = await res.json()
    if (data.candidate) {
      await pc.addIceCandidate(data.candidate)
    }
  }, 1000)
}
</script>

<template>
  <!-- <div>
    <NuxtRouteAnnouncer />
    <NuxtWelcome />
  </div> -->
    <div>
        <h2>WebRTC Audio Only</h2>
        <button @click="start(true)">Start as Caller</button>
        <button @click="start(false)">Start as Callee</button>
    </div>
</template>
