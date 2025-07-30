package main

import (
	"golang-webrtc/controllers"

	"github.com/labstack/echo/v4"
)

// var upgrader = websocket.Upgrader{
// 	CheckOrigin: func(r *http.Request) bool {
// 		return true
// 	},
// }

// var peers = make(map[string]*Peer)
// var lock sync.Mutex

// Message from/to client
// type SignalMessage struct {
// 	Type      string                   `json:"type"`
// 	SDP       string                   `json:"sdp,omitempty"`
// 	Candidate *webrtc.ICECandidateInit `json:"candidate,omitempty"`
// }

// type Peer struct {
// 	WebsocketConn *websocket.Conn
// 	Conn          *webrtc.PeerConnection
// 	AudioTrack    *webrtc.TrackLocalStaticRTP
// }

func main() {
	e := echo.New()

	e.Static("/", "static")
	e.GET("/ws", controllers.HandleWebSocket)
	e.GET("/ws-video", controllers.HandleWebSocketVideo)
	e.GET("/ws-record-audio", controllers.HandleWebSocketRecordAudio)
	e.GET("/ws-record-video", controllers.HandleWebSocketRecordVideo)

	e.Logger.Fatal(e.Start(":8080"))
}

// func handleWebSocket(c echo.Context) error {
// 	conn, err := upgrader.Upgrade(c.Response(), c.Request(), nil)
// 	if err != nil {
// 		return err
// 	}
// 	defer conn.Close()

// 	// WebRTC configuration
// 	peerConnection, err := webrtc.NewPeerConnection(webrtc.Configuration{
// 		ICEServers: []webrtc.ICEServer{
// 			{URLs: []string{"stun:stun.l.google.com:19302"}},
// 		},
// 	})
// 	if err != nil {
// 		log.Println("Failed to create PeerConnection:", err)
// 		return err
// 	}
// 	defer peerConnection.Close()

// 	// Buat track lokal untuk audio dari remote peer
// 	localTrack, err := webrtc.NewTrackLocalStaticRTP(
// 		webrtc.RTPCodecCapability{MimeType: webrtc.MimeTypeOpus},
// 		"audio", "relay",
// 	)
// 	if err != nil {
// 		return err
// 	}

// 	// Simpan peer
// 	peerId := uuid.New().String()
// 	lock.Lock()
// 	peers[peerId] = &Peer{WebsocketConn: conn, Conn: peerConnection, AudioTrack: localTrack}
// 	lock.Unlock()

// 	// Tambahkan track relay ke peer ini
// 	_, err = peerConnection.AddTrack(localTrack)
// 	if err != nil {
// 		log.Println("AddTrack error:", err)
// 	}

// 	// Receive remote track (e.g. audio from browser)
// 	peerConnection.OnTrack(func(track *webrtc.TrackRemote, receiver *webrtc.RTPReceiver) {
// 		log.Printf("Received track: %s\n", track.Codec().MimeType)
// 		//log.Println("🎙️ Audio track received")

// 		go func() {
// 			for {
// 				pkt, _, err := track.ReadRTP()
// 				if err != nil {
// 					log.Println("pkt, _, err := track.ReadRTP() err:", err)
// 					break
// 				}

// 				// Kirim ke semua peer lain
// 				lock.Lock()
// 				for k, peer := range peers {
// 					if k != peerId { // jangan kirim ke pengirim sendiri
// 						err = peer.AudioTrack.WriteRTP(pkt)
// 						if err != nil {
// 							log.Println("peer.AudioTrack.WriteRTP(pkt) err:", err)
// 						}
// 					}
// 				}
// 				lock.Unlock()
// 			}
// 		}()
// 	})

// 	// Handle ICE candidates from Go → Browser
// 	peerConnection.OnICECandidate(func(candidate *webrtc.ICECandidate) {
// 		if candidate == nil {
// 			return
// 		}
// 		log.Println("Sending ICE candidate to client")
// 		candidateJson := candidate.ToJSON()
// 		msg := SignalMessage{
// 			Type:      "ice-candidate",
// 			Candidate: &candidateJson,
// 		}
// 		conn.WriteJSON(msg)
// 	})

// 	//// Receive remote track (e.g. audio from browser)
// 	//peerConnection.OnTrack(func(track *webrtc.TrackRemote, receiver *webrtc.RTPReceiver) {
// 	//	log.Printf("Received track: %s\n", track.Codec().MimeType)
// 	//})

// 	// Read loop for signaling messages from client
// 	for {
// 		_, message, err := conn.ReadMessage()
// 		if err != nil {
// 			log.Println("WebSocket read error:", err)
// 			break
// 		}
// 		//fmt.Println("message readmessage:", message)

// 		var signal SignalMessage
// 		if err := json.Unmarshal(message, &signal); err != nil {
// 			log.Println("Invalid signal:", err)
// 			continue
// 		}

// 		switch signal.Type {
// 		case "offer":
// 			log.Println("Received offer from client")
// 			offer := webrtc.SessionDescription{
// 				Type: webrtc.SDPTypeOffer,
// 				SDP:  signal.SDP,
// 			}
// 			if err := peerConnection.SetRemoteDescription(offer); err != nil {
// 				log.Println("SetRemoteDescription error:", err)
// 				continue
// 			}

// 			answer, err := peerConnection.CreateAnswer(nil)
// 			if err != nil {
// 				log.Println("CreateAnswer error:", err)
// 				continue
// 			}
// 			if err := peerConnection.SetLocalDescription(answer); err != nil {
// 				log.Println("SetLocalDescription error:", err)
// 				continue
// 			}

// 			// Kirim answer ke client
// 			conn.WriteJSON(SignalMessage{
// 				Type: "answer",
// 				SDP:  answer.SDP,
// 			})

// 		case "ice-candidate":
// 			if signal.Candidate != nil {
// 				log.Println("Received ICE candidate from client")
// 				if err := peerConnection.AddICECandidate(*signal.Candidate); err != nil {
// 					log.Println("AddICECandidate error:", err)
// 				}
// 			}
// 		}
// 	}

// 	// Cleanup saat disconnect
// 	lock.Lock()
// 	delete(peers, peerId)
// 	lock.Unlock()

// 	log.Println("🔌 Client disconnected")
// 	return nil
// }

// func handleWebSocketVideo(c echo.Context) error {
// 	conn, err := upgrader.Upgrade(c.Response(), c.Request(), nil)
// 	if err != nil {
// 		return err
// 	}
// 	defer conn.Close()

// 	// WebRTC configuration
// 	peerConnection, err := webrtc.NewPeerConnection(webrtc.Configuration{
// 		ICEServers: []webrtc.ICEServer{
// 			{URLs: []string{"stun:stun.l.google.com:19302"}},
// 		},
// 	})
// 	if err != nil {
// 		log.Println("Failed to create PeerConnection:", err)
// 		return err
// 	}
// 	defer peerConnection.Close()

// 	// Buat track lokal untuk audio dari remote peer
// 	localTrack, err := webrtc.NewTrackLocalStaticRTP(
// 		webrtc.RTPCodecCapability{MimeType: webrtc.MimeTypeOpus},
// 		"audio", "relay",
// 	)
// 	if err != nil {
// 		return err
// 	}

// 	// Simpan peer
// 	peerId := uuid.New().String()
// 	lock.Lock()
// 	peers[peerId] = &Peer{WebsocketConn: conn, Conn: peerConnection, AudioTrack: localTrack}
// 	lock.Unlock()

// 	// Tambahkan track relay ke peer ini
// 	_, err = peerConnection.AddTrack(localTrack)
// 	if err != nil {
// 		log.Println("AddTrack error:", err)
// 	}

// 	// Receive remote track (e.g. audio from browser)
// 	peerConnection.OnTrack(func(track *webrtc.TrackRemote, receiver *webrtc.RTPReceiver) {
// 		log.Printf("Received track: %s\n", track.Codec().MimeType)
// 		//log.Println("🎙️ Audio track received")

// 		go func() {
// 			for {
// 				pkt, _, err := track.ReadRTP()
// 				if err != nil {
// 					log.Println("pkt, _, err := track.ReadRTP() err:", err)
// 					break
// 				}

// 				// Kirim ke semua peer lain
// 				lock.Lock()
// 				for k, peer := range peers {
// 					if k != peerId { // jangan kirim ke pengirim sendiri
// 						err = peer.AudioTrack.WriteRTP(pkt)
// 						if err != nil {
// 							log.Println("peer.AudioTrack.WriteRTP(pkt) err:", err)
// 						}
// 					}
// 				}
// 				lock.Unlock()
// 			}
// 		}()
// 	})

// 	// Handle ICE candidates from Go → Browser
// 	peerConnection.OnICECandidate(func(candidate *webrtc.ICECandidate) {
// 		if candidate == nil {
// 			return
// 		}
// 		log.Println("Sending ICE candidate to client")
// 		candidateJson := candidate.ToJSON()
// 		msg := SignalMessage{
// 			Type:      "ice-candidate",
// 			Candidate: &candidateJson,
// 		}
// 		conn.WriteJSON(msg)
// 	})

// 	//// Receive remote track (e.g. audio from browser)
// 	//peerConnection.OnTrack(func(track *webrtc.TrackRemote, receiver *webrtc.RTPReceiver) {
// 	//	log.Printf("Received track: %s\n", track.Codec().MimeType)
// 	//})

// 	// Read loop for signaling messages from client
// 	for {
// 		_, message, err := conn.ReadMessage()
// 		if err != nil {
// 			log.Println("WebSocket read error:", err)
// 			break
// 		}
// 		//fmt.Println("message readmessage:", message)

// 		var signal SignalMessage
// 		if err := json.Unmarshal(message, &signal); err != nil {
// 			log.Println("Invalid signal:", err)
// 			continue
// 		}

// 		switch signal.Type {
// 		case "offer":
// 			log.Println("Received offer from client")
// 			offer := webrtc.SessionDescription{
// 				Type: webrtc.SDPTypeOffer,
// 				SDP:  signal.SDP,
// 			}
// 			if err := peerConnection.SetRemoteDescription(offer); err != nil {
// 				log.Println("SetRemoteDescription error:", err)
// 				continue
// 			}

// 			answer, err := peerConnection.CreateAnswer(nil)
// 			if err != nil {
// 				log.Println("CreateAnswer error:", err)
// 				continue
// 			}
// 			if err := peerConnection.SetLocalDescription(answer); err != nil {
// 				log.Println("SetLocalDescription error:", err)
// 				continue
// 			}

// 			// Kirim answer ke client
// 			conn.WriteJSON(SignalMessage{
// 				Type: "answer",
// 				SDP:  answer.SDP,
// 			})

// 		case "ice-candidate":
// 			if signal.Candidate != nil {
// 				log.Println("Received ICE candidate from client")
// 				if err := peerConnection.AddICECandidate(*signal.Candidate); err != nil {
// 					log.Println("AddICECandidate error:", err)
// 				}
// 			}
// 		}
// 	}

// 	// Cleanup saat disconnect
// 	lock.Lock()
// 	delete(peers, peerId)
// 	lock.Unlock()

// 	log.Println("🔌 Client disconnected")
// 	return nil
// }
