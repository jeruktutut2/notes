package controllers

import (
	"encoding/binary"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"

	"github.com/google/uuid"
	"github.com/gorilla/websocket"
	"github.com/hraban/opus"
	"github.com/labstack/echo/v4"
	"github.com/pion/webrtc/v4"
)

var upgraderRecordAudio = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

type PeerRecordAudio struct {
	WebsocketConn *websocket.Conn
	Conn          *webrtc.PeerConnection
	AudioTrack    *webrtc.TrackLocalStaticRTP
}

// Message from/to client
type SignalMessageRecordAudio struct {
	Type      string                   `json:"type"`
	SDP       string                   `json:"sdp,omitempty"`
	Candidate *webrtc.ICECandidateInit `json:"candidate,omitempty"`
}

var peerRecordAudios = make(map[string]*PeerRecordAudio)
var lockRecordAudio sync.Mutex
var wavWriterRecordAudios = make(map[string]*os.File)
var multiAudioOnceRecordAudio sync.Once
var multiAudioWavRecordAudio *os.File
var multiAudioWavMutexRecordAudio sync.Mutex
var multiAudioDecoderRecordAudio *opus.Decoder
var multiAudioLockRecordAudio sync.Mutex
var multiAudioFileRecordAudio *os.File

func writeWavHeader(f *os.File) {
	sampleRate := uint32(48000)
	bitsPerSample := uint16(16)
	channels := uint16(1)
	byteRate := sampleRate * uint32(channels) * uint32(bitsPerSample) / 8
	blockAlign := channels * bitsPerSample / 8
	dataSize := uint32(0xffffffff) // placeholder for infinite stream

	f.Write([]byte("RIFF"))
	binary.Write(f, binary.LittleEndian, dataSize+36)
	f.Write([]byte("WAVE"))
	f.Write([]byte("fmt "))
	binary.Write(f, binary.LittleEndian, uint32(16))
	binary.Write(f, binary.LittleEndian, uint16(1)) // PCM
	binary.Write(f, binary.LittleEndian, channels)
	binary.Write(f, binary.LittleEndian, sampleRate)
	binary.Write(f, binary.LittleEndian, byteRate)
	binary.Write(f, binary.LittleEndian, blockAlign)
	binary.Write(f, binary.LittleEndian, bitsPerSample)
	f.Write([]byte("data"))
	binary.Write(f, binary.LittleEndian, dataSize)
}

func HandleWebSocketRecordAudio(c echo.Context) error {
	conn, err := upgraderRecordAudio.Upgrade(c.Response(), c.Request(), nil)
	if err != nil {
		return err
	}
	defer conn.Close()

	// WebRTC configuration
	peerConnection, err := webrtc.NewPeerConnection(webrtc.Configuration{
		ICEServers: []webrtc.ICEServer{
			{URLs: []string{"stun:stun.l.google.com:19302"}},
		},
	})
	if err != nil {
		log.Println("Failed to create PeerConnection:", err)
		return err
	}
	defer peerConnection.Close()

	// Buat track lokal untuk audio dari remote peer
	localTrack, err := webrtc.NewTrackLocalStaticRTP(
		webrtc.RTPCodecCapability{MimeType: webrtc.MimeTypeOpus},
		"audio", "relay",
	)
	if err != nil {
		return err
	}

	// Simpan peer
	peerId := uuid.New().String()
	lockRecordAudio.Lock()
	peerRecordAudios[peerId] = &PeerRecordAudio{WebsocketConn: conn, Conn: peerConnection, AudioTrack: localTrack}
	lockRecordAudio.Unlock()

	// Tambahkan track relay ke peer ini
	_, err = peerConnection.AddTrack(localTrack)
	if err != nil {
		log.Println("AddTrack error:", err)
	}

	// Receive remote track (e.g. audio from browser)
	peerConnection.OnTrack(func(track *webrtc.TrackRemote, receiver *webrtc.RTPReceiver) {
		log.Printf("Received track: %s\n", track.Codec().MimeType)
		//log.Println("🎙️ Audio track received")

		// create audio file
		if track.Kind() == webrtc.RTPCodecTypeAudio {
			// decoder, err := opus.NewDecoder(48000, 1)
			// if err != nil {
			// 	log.Printf("Failed to create Opus decoder: %v", err)
			// 	return
			// }

			wavFilename := fmt.Sprintf("recordings/audio-%s.wav", peerId)
			wavFile, err := os.Create(wavFilename)
			if err != nil {
				log.Printf("Failed to create WAV file: %v", err)
				return
			}
			writeWavHeader(wavFile)
			wavWriterRecordAudios[peerId] = wavFile

			multiAudioOnceRecordAudio.Do(func() {
				multiAudioFileRecordAudio, _ = os.Create("recordings/all-audio.rtp")
				multiAudioWavRecordAudio, _ = os.Create("recordings/all-audio.wav")
				writeWavHeader(multiAudioWavRecordAudio)
				multiAudioDecoderRecordAudio, _ = opus.NewDecoder(48000, 1)
			})

			go func() {
				defer wavFile.Close()
				for {
					rtp, _, err := track.ReadRTP()
					if err != nil {
						break
					}
					multiAudioLockRecordAudio.Lock()
					raw, _ := rtp.Marshal()
					multiAudioFileRecordAudio.Write(raw)
					multiAudioLockRecordAudio.Unlock()

					pcm := make([]int16, 960)
					if n, err := multiAudioDecoderRecordAudio.Decode(rtp.Payload, pcm); err == nil {
						for i := 0; i < n; i++ {
							binary.Write(wavFile, binary.LittleEndian, pcm[i])
						}
						multiAudioWavMutexRecordAudio.Lock()
						for i := 0; i < n; i++ {
							binary.Write(multiAudioWavRecordAudio, binary.LittleEndian, pcm[i])
						}
						multiAudioWavMutexRecordAudio.Unlock()
					}
				}
			}()
		}

		go func() {
			for {
				pkt, _, err := track.ReadRTP()
				if err != nil {
					log.Println("pkt, _, err := track.ReadRTP() err:", err)
					break
				}

				// Kirim ke semua peer lain
				lockRecordAudio.Lock()
				for k, peer := range peerRecordAudios {
					if k != peerId { // jangan kirim ke pengirim sendiri
						if track.Kind() == webrtc.RTPCodecTypeAudio {
							err = peer.AudioTrack.WriteRTP(pkt)
							if err != nil {
								log.Println("peer.AudioTrack.WriteRTP(pkt) err:", err)
							}
						}
					}
				}
				lockRecordAudio.Unlock()
			}
		}()
	})

	// Handle ICE candidates from Go → Browser
	peerConnection.OnICECandidate(func(candidate *webrtc.ICECandidate) {
		if candidate == nil {
			return
		}
		log.Println("Sending ICE candidate to client")
		candidateJson := candidate.ToJSON()
		msg := SignalMessageRecordAudio{
			Type:      "ice-candidate",
			Candidate: &candidateJson,
		}
		conn.WriteJSON(msg)
	})

	//// Receive remote track (e.g. audio from browser)
	//peerConnection.OnTrack(func(track *webrtc.TrackRemote, receiver *webrtc.RTPReceiver) {
	//	log.Printf("Received track: %s\n", track.Codec().MimeType)
	//})

	// Read loop for signaling messages from client
	for {
		_, message, err := conn.ReadMessage()
		if err != nil {
			log.Println("WebSocket read error:", err)
			break
		}
		//fmt.Println("message readmessage:", message)

		var signal SignalMessageRecordAudio
		if err := json.Unmarshal(message, &signal); err != nil {
			log.Println("Invalid signal:", err)
			continue
		}

		switch signal.Type {
		case "offer":
			log.Println("Received offer from client")
			offer := webrtc.SessionDescription{
				Type: webrtc.SDPTypeOffer,
				SDP:  signal.SDP,
			}
			if err := peerConnection.SetRemoteDescription(offer); err != nil {
				log.Println("SetRemoteDescription error:", err)
				continue
			}

			answer, err := peerConnection.CreateAnswer(nil)
			if err != nil {
				log.Println("CreateAnswer error:", err)
				continue
			}
			if err := peerConnection.SetLocalDescription(answer); err != nil {
				log.Println("SetLocalDescription error:", err)
				continue
			}

			// Kirim answer ke client
			conn.WriteJSON(SignalMessageRecordAudio{
				Type: "answer",
				SDP:  answer.SDP,
			})

		case "ice-candidate":
			if signal.Candidate != nil {
				log.Println("Received ICE candidate from client")
				if err := peerConnection.AddICECandidate(*signal.Candidate); err != nil {
					log.Println("AddICECandidate error:", err)
				}
			}
		}
	}

	// Cleanup saat disconnect
	lockRecordAudio.Lock()
	delete(peerRecordAudios, peerId)
	if wav, ok := wavWriterRecordAudios[peerId]; ok {
		wav.Close()
		delete(wavWriterRecordAudios, peerId)
	}
	lockRecordAudio.Unlock()

	log.Println("🔌 Client disconnected")
	return nil
}
