package main

import (
	"fmt"
	"net/http"
	"sync"

	"github.com/gorilla/websocket"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

// Upgrader untuk mengubah HTTP menjadi WebSocket
var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		return true // Mengizinkan semua koneksi
	},
}

// Map untuk menyimpan koneksi WebSocket berdasarkan client ID
var clients = make(map[string]*websocket.Conn)
var clientsMutex sync.Mutex

func main() {
	e := echo.New()
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins: []string{"*"},
		AllowHeaders: []string{echo.HeaderOrigin, echo.HeaderContentType, echo.HeaderAccept},
	}))
	e.GET("/ws", func(c echo.Context) error {
		clientID := c.QueryParam("id") // Ambil ID dari query parameter
		if clientID == "" {
			return c.String(http.StatusBadRequest, "Client ID diperlukan")
		}

		// Upgrade koneksi HTTP menjadi WebSocket
		ws, err := upgrader.Upgrade(c.Response(), c.Request(), nil)
		if err != nil {
			fmt.Println("Gagal upgrade ke WebSocket:", err)
			return err
		}
		defer ws.Close()

		// Simpan koneksi ke dalam map
		clientsMutex.Lock()
		clients[clientID] = ws
		clientsMutex.Unlock()
		fmt.Println("clients:", clients)

		<-c.Request().Context().Done()

		// Hapus client dari map saat terputus
		clientsMutex.Lock()
		delete(clients, clientID)
		clientsMutex.Unlock()

		fmt.Println("Client", clientID, "terputus")
		return nil
	})

	// Handler untuk mengirim pesan ke client tertentu
	e.GET("send-message", func(c echo.Context) error {
		clientIdSendTo := c.QueryParam("clientIdSendTo") // Ambil ID dari query
		message := c.QueryParam("msg")                   // Ambil pesan dari query
		fmt.Println("message:", clientIdSendTo, message)

		clientsMutex.Lock()
		conn, exists := clients[clientIdSendTo]
		clientsMutex.Unlock()

		if !exists {
			return c.String(http.StatusNotFound, "Client tidak ditemukan")
		}

		// Kirim pesan ke client yang dipilih
		err := conn.WriteMessage(websocket.TextMessage, []byte(message))
		if err != nil {
			return c.String(http.StatusInternalServerError, "Gagal mengirim pesan")
		}

		return c.String(http.StatusOK, "Pesan terkirim ke "+clientIdSendTo)
	})

	// Menjalankan server
	fmt.Println("Server berjalan di :8080...")
	e.Logger.Fatal(e.Start(":8080"))
}
