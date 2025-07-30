package main

import (
	"embed"
	"encoding/hex"
	"encoding/json"
	"fmt"
	go_webrtcvad "github.com/aflyingHusky/go-webrtcvad"
	"github.com/gorilla/websocket"
	"github.com/labstack/echo/v4"
	"github.com/pion/opus"
	"github.com/pion/webrtc/v4"
	"io"
	"io/fs"
	"log"
	"net/http"
)

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true
	},
}

type SignalMessage struct {
	Type      string                   `json:"type"`
	SDP       string                   `json:"sdp,omitempty"`
	Candidate *webrtc.ICECandidateInit `json:"candidate,omitempty"`
}

//go:embed static/*
var embeddedFiles embed.FS

func main() {
	e := echo.New()
	staticFiles, _ := fs.Sub(embeddedFiles, "static")
	e.GET("/ws-vad", wsVad)
	e.GET("/*", echo.WrapHandler(http.FileServer(http.FS(staticFiles))))
	e.Logger.Fatal(e.Start(":8080"))
}

func wsVad(c echo.Context) error {
	conn, err := upgrader.Upgrade(c.Response(), c.Request(), nil)
	if err != nil {
		return err
	}
	defer conn.Close()

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

	localTrack, err := webrtc.NewTrackLocalStaticRTP(
		webrtc.RTPCodecCapability{MimeType: webrtc.MimeTypeOpus},
		"audio", "relay",
	)
	if err != nil {
		return err
	}

	_, err = peerConnection.AddTrack(localTrack)
	if err != nil {
		log.Println("AddTrack error:", err)
	}

	peerConnection.OnTrack(func(track *webrtc.TrackRemote, receiver *webrtc.RTPReceiver) {
		log.Printf("Received track: %s\n", track.Codec().MimeType)

		vad, err := go_webrtcvad.New()
		if err != nil {
			log.Fatalf("Gagal inisialisasi VAD: %v", err)
		}
		//defer vad.Free()
		vad.SetMode(0)

		go func() {
			for {
				fmt.Println("Track kind:", track.Kind())
				fmt.Println("Track codec:", track.Codec().MimeType)
				if track.Kind() != webrtc.RTPCodecTypeAudio || track.Codec().MimeType != webrtc.MimeTypeOpus {
					fmt.Println("Skipping track, not audio/opus")
					return
				}
				fmt.Println("Got track!")
				fmt.Println("Kind:", track.Kind())
				fmt.Println("Codec:", track.Codec().MimeType)
				fmt.Println("SSRC:", track.SSRC())

				pkt, _, err := track.ReadRTP()
				if err != nil {
					if err == io.EOF {
						log.Println("EOF: Stream audio berakhir.")
						break
					}
					log.Println("pkt, _, err := track.ReadRTP() err:", err)
					break
				}
				//fmt.Println("pkt:", pkt)
				fmt.Println("pkt.Payload:", pkt.Payload)
				fmt.Println("Opus payload length:", len(pkt.Payload))
				fmt.Printf("First 8 bytes: % x\n", pkt.Payload[:8])
				fmt.Printf("First 10 bytes: % x\n", pkt.Payload[:10])

				//err = localTrack.WriteRTP(pkt)
				//if err != nil {
				//	log.Println("localTrack.WriteRTP(pkt) err:", err)
				//}

				//DebugOpusPayload(pkt.Payload)

				//var packet rtp.Packet
				//err = packet.Unmarshal(pkt.Payload)
				//if err != nil {
				//	fmt.Println("packet err:", err)
				//	break
				//}
				//fmt.Println("packet:", packet)

				//var pcmbuffer []byte
				decoder := opus.NewDecoder()
				if err != nil {
					fmt.Println("opus.NewDecoder err:", err)
				}
				//fmt.Println("decoder, err :", decoder, err)

				//var pcm []byte
				pcm := make([]byte, 960*2)
				bandwith, isStereo, err := decoder.Decode(pkt.Payload, pcm)
				if err != nil {
					log.Println("decoder.Decode err:", err)
					break
				}
				fmt.Println("decoder.Decode:", bandwith, isStereo, err)

				//int16SliceToBytes(pcmsamples)
				//activeVoice, err := vad.Process(48000, pcmbuffer)
				//if err != nil {
				//	log.Println("vad.Process err:", activeVoice, err)
				//	break
				//}
				//log.Println("vad.Process:", activeVoice, err)

				err = localTrack.WriteRTP(pkt)
				if err != nil {
					log.Println("localTrack.WriteRTP(pkt) err:", err)
				}
			}
		}()
	})

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

	return nil
}

func DebugOpusPayload(payload []byte) {
	fmt.Printf("Payload Length: %d\n", len(payload))
	fmt.Printf("Payload Hex: %s\n", hex.EncodeToString(payload[:min(16, len(payload))]))

	if len(payload) > 0 {
		// Byte pertama berisi informasi konfigurasi Opus
		configByte := payload[0]
		fmt.Printf("Config Byte: 0x%02x (%08b)\n", configByte, configByte)

		// Parse Opus TOC (Table of Contents)
		config := (configByte >> 3) & 0x1F // bits 3-7
		stereo := (configByte >> 2) & 0x01 // bit 2
		frameCount := configByte & 0x03    // bits 0-1

		fmt.Printf("Opus Config: %d, Stereo: %d, Frame Count Code: %d\n",
			config, stereo, frameCount)
	}
}

func int16SliceToBytes(samples []int16) []byte {
	bytes := make([]byte, len(samples)*2)
	for i, sample := range samples {
		// Little endian conversion
		bytes[i*2] = byte(sample & 0xFF)
		bytes[i*2+1] = byte((sample >> 8) & 0xFF)
	}
	return bytes
}
