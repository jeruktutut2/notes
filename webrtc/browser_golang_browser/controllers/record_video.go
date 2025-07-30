package controllers

import (
	"encoding/json"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"os/exec"
	"sync"

	"github.com/google/uuid"
	"github.com/gorilla/websocket"
	"github.com/labstack/echo/v4"
	"github.com/pion/webrtc/v4"
)

var upgraderRecordVideo = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

type PeerRecordVideo struct {
	WebsocketConn *websocket.Conn
	Conn          *webrtc.PeerConnection
	VideoTrack    *webrtc.TrackLocalStaticRTP
	AudioTrack    *webrtc.TrackLocalStaticRTP
}

type SignalMessageRecordVideo struct {
	Type      string                   `json:"type"`
	SDP       string                   `json:"sdp,omitempty"`
	Candidate *webrtc.ICECandidateInit `json:"candidate,omitempty"`
}

type RecordingSession struct {
	VideoPort int
	AudioPort int
	Cmd       *exec.Cmd
}

var peerRecordVideos = make(map[string]*PeerRecordVideo)
var ffmpegSessions = make(map[string]*RecordingSession)
var lockRecordVideo sync.Mutex

func ensureRecordingDir() error {
	const path = "./recordings"
	if _, err := os.Stat(path); os.IsNotExist(err) {
		return os.MkdirAll(path, 0755)
	}
	return nil
}

func getFreeUDPPorts() (int, int, error) {
	getPort := func() (int, error) {
		addr, err := net.ResolveUDPAddr("udp", "localhost:0")
		if err != nil {
			return 0, err
		}
		l, err := net.ListenUDP("udp", addr)
		if err != nil {
			return 0, err
		}
		defer l.Close()
		return l.LocalAddr().(*net.UDPAddr).Port, nil
	}

	videoPort, err := getPort()
	if err != nil {
		return 0, 0, err
	}
	audioPort, err := getPort()
	if err != nil {
		return 0, 0, err
	}
	return videoPort, audioPort, nil
}

func startFFmpegForPeer(peerId string, videoPort, audioPort int) (*exec.Cmd, error) {
	if err := ensureRecordingDir(); err != nil {
		return nil, fmt.Errorf("failed to create recordings folder: %w", err)
	}

	outputFile := fmt.Sprintf("recordings/recorded_%s.webm", peerId)

	cmd := exec.Command("ffmpeg",
		"-protocol_whitelist", "file,udp,rtp",
		"-f", "rtp", "-i", fmt.Sprintf("udp://127.0.0.1:%d", videoPort),
		"-f", "rtp", "-i", fmt.Sprintf("udp://127.0.0.1:%d", audioPort),
		"-c:v", "copy",
		"-c:a", "copy",
		"-y", outputFile,
	)

	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	err := cmd.Start()
	if err != nil {
		return nil, err
	}
	log.Printf("📼 Started ffmpeg → %s", outputFile)
	return cmd, nil
}

func HandleWebSocketRecordVideo(c echo.Context) error {
	conn, err := upgraderRecordVideo.Upgrade(c.Response(), c.Request(), nil)
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
	lockRecordVideo.Lock()
	peerRecordVideos[peerId] = &PeerRecordVideo{WebsocketConn: conn, Conn: peerConnection, VideoTrack: videoTrack, AudioTrack: audioTrack}
	lockRecordVideo.Unlock()

	// Tambahkan track relay ke peer ini
	_, err = peerConnection.AddTrack(videoTrack)
	if err != nil {
		log.Println("AddTrack error:", err)
	}
	_, err = peerConnection.AddTrack(audioTrack)
	if err != nil {
		log.Println("AddTrack audio error:", err)
	}

	videoPort, audioPort, err := getFreeUDPPorts()
	if err != nil {
		log.Println("Failed to get free ports:", err)
		return err
	}
	cmd, err := startFFmpegForPeer(peerId, videoPort, audioPort)
	fmt.Println("startFFmpegForPeer(peerId, videoPort, audioPort):", peerId, videoPort, audioPort, err)
	if err == nil {
		ffmpegSessions[peerId] = &RecordingSession{VideoPort: videoPort, AudioPort: audioPort, Cmd: cmd}
	} else {
		log.Printf("❌ Failed to start ffmpeg for %s: %v", peerId, err)
		return err
	}

	// Receive remote track (e.g. audio from browser)
	peerConnection.OnTrack(func(track *webrtc.TrackRemote, receiver *webrtc.RTPReceiver) {
		log.Printf("Received track: %s\n", track.Codec().MimeType)
		//log.Println("🎙️ Audio track received")

		session, ok := ffmpegSessions[peerId]
		if !ok {
			log.Println("❌ No ffmpeg session for peer", peerId)
			return
		}

		var port int
		switch track.Kind() {
		case webrtc.RTPCodecTypeVideo:
			port = session.VideoPort
		case webrtc.RTPCodecTypeAudio:
			port = session.AudioPort
		default:
			return
		}

		udpConn, err := net.Dial("udp", fmt.Sprintf("127.0.0.1:%d", port))
		if err != nil {
			log.Println("UDP Dial error:", err)
			return
		}

		go func() {
			for {
				defer udpConn.Close()

				pkt, _, err := track.ReadRTP()
				if err != nil {
					log.Println("pkt, _, err := track.ReadRTP() err:", err)
					break
				}

				raw, _ := pkt.Marshal()
				udpConn.Write(raw)

				// Kirim ke semua peer lain
				lockRecordVideo.Lock()
				for k, peer := range peerRecordVideos {
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
				lockRecordVideo.Unlock()
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

		var signal SignalMessageRecordVideo
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
	lockRecordVideo.Lock()
	delete(peerRecordVideos, peerId)
	lockRecordVideo.Unlock()

	if session, ok := ffmpegSessions[peerId]; ok {
		if session.Cmd != nil {
			_ = session.Cmd.Process.Kill()
		}
		delete(ffmpegSessions, peerId)
	}

	log.Println("🔌 Client disconnected")
	return nil
}
