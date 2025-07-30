package controllers

import (
	"encoding/json"
	"log"
	"net/http"
	"sync"

	"github.com/google/uuid"
	"github.com/gorilla/websocket"
	"github.com/labstack/echo/v4"
	"github.com/pion/webrtc/v4"
)

var upgraderVideo = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

type PeerVideo struct {
	WebsocketConn *websocket.Conn
	Conn          *webrtc.PeerConnection
	VideoTrack    *webrtc.TrackLocalStaticRTP
	AudioTrack    *webrtc.TrackLocalStaticRTP
}

type SignalMessageVideo struct {
	Type      string                   `json:"type"`
	SDP       string                   `json:"sdp,omitempty"`
	Candidate *webrtc.ICECandidateInit `json:"candidate,omitempty"`
}

var peerVideos = make(map[string]*PeerVideo)
var lockVideo sync.Mutex

func HandleWebSocketVideo(c echo.Context) error {
	conn, err := upgraderVideo.Upgrade(c.Response(), c.Request(), nil)
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
	// videoTrack, err := webrtc.NewTrackLocalStaticRTP(
	// 	webrtc.RTPCodecCapability{MimeType: webrtc.MimeTypeOpus},
	// 	"audio", "relay",
	// )
	videoTrack, _ := webrtc.NewTrackLocalStaticRTP(webrtc.RTPCodecCapability{MimeType: webrtc.MimeTypeVP8}, "video", "pion")
	// if err != nil {
	// 	return err
	// }
	audioTrack, _ := webrtc.NewTrackLocalStaticRTP(webrtc.RTPCodecCapability{MimeType: webrtc.MimeTypeOpus}, "audio", "pion")

	// Simpan peer
	peerId := uuid.New().String()
	lockVideo.Lock()
	peerVideos[peerId] = &PeerVideo{WebsocketConn: conn, Conn: peerConnection, VideoTrack: videoTrack, AudioTrack: audioTrack}
	lockVideo.Unlock()

	// Tambahkan track relay ke peer ini
	_, err = peerConnection.AddTrack(videoTrack)
	if err != nil {
		log.Println("AddTrack error:", err)
	}
	_, err = peerConnection.AddTrack(audioTrack)
	if err != nil {
		log.Println("AddTrack audio error:", err)
	}

	// Receive remote track (e.g. audio from browser)
	peerConnection.OnTrack(func(track *webrtc.TrackRemote, receiver *webrtc.RTPReceiver) {
		log.Printf("Received track: %s\n", track.Codec().MimeType)
		//log.Println("🎙️ Audio track received")

		go func() {
			for {
				pkt, _, err := track.ReadRTP()
				if err != nil {
					log.Println("pkt, _, err := track.ReadRTP() err:", err)
					break
				}

				// Kirim ke semua peer lain
				lockVideo.Lock()
				for k, peer := range peerVideos {
					if k != peerId { // jangan kirim ke pengirim sendiri
						if track.Kind() == webrtc.RTPCodecTypeVideo {
							err = peer.VideoTrack.WriteRTP(pkt)
							if err != nil {
								log.Println("peer.VideoTrack.WriteRTP(pkt) err:", err)
							}
						} else if track.Kind() == webrtc.RTPCodecTypeAudio {
							err = peer.AudioTrack.WriteRTP(pkt)
							if err != nil {
								log.Println("peer.VideoTrack.WriteRTP(pkt) err:", err)
							}
						}
					}
				}
				lockVideo.Unlock()
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
		msg := SignalMessage{
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

		var signal SignalMessage
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
			conn.WriteJSON(SignalMessage{
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
	lockVideo.Lock()
	delete(peerVideos, peerId)
	lockVideo.Unlock()

	log.Println("🔌 Client disconnected")
	return nil
}
