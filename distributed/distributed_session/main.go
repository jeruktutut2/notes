package main

import (
	"log"
	"net/http"
	"os"
	"time"

	"distributed_session/internal/session"

	"github.com/google/uuid"
	"github.com/labstack/echo/v4"
)

func main() {
	e := echo.New()

	redisURL := os.Getenv("REDIS_URL")
	if redisURL == "" {
		redisURL = "redis://localhost:6381/0"
	}

	sessionStore := session.NewRedisSessionStore(redisURL)

	// Route 1: Login (Membuat Session)
	e.POST("/login", func(c echo.Context) error {
		// Asumsi autentikasi sukses (username/password benar)
		sessionID := uuid.New().String()

		userData := session.UserSession{
			UserID:    "USR-999",
			Username:  "johndoe",
			Role:      "admin",
			LoginTime: time.Now().Format(time.RFC3339),
		}

		// Simpan di Redis dengan TTL 30 menit
		err := sessionStore.CreateSession(c.Request().Context(), sessionID, userData, 30*time.Minute)
		if err != nil {
			return c.JSON(http.StatusInternalServerError, map[string]string{"error": "Gagal membuat session"})
		}

		// Kembalikan sessionID ke client (biasanya via Cookie, di sini via JSON demi kesederhanaan)
		return c.JSON(http.StatusOK, map[string]string{
			"message":    "Login berhasil!",
			"session_id": sessionID,
		})
	})

	// Route 2: Proteksi endpoint (Cek Session)
	e.GET("/profile", func(c echo.Context) error {
		sessionID := c.Request().Header.Get("X-Session-ID")
		if sessionID == "" {
			return c.JSON(http.StatusUnauthorized, map[string]string{"error": "Missing X-Session-ID"})
		}

		// Ambil data session dari Centralized Redis
		userData, err := sessionStore.GetSession(c.Request().Context(), sessionID)
		if err != nil {
			return c.JSON(http.StatusUnauthorized, map[string]string{"error": "Session expired atau tidak valid"})
		}

		// Sliding Expiration: Refresh TTL karena user sedang aktif
		sessionStore.RefreshSession(c.Request().Context(), sessionID, 30*time.Minute)

		return c.JSON(http.StatusOK, map[string]any{
			"message": "Selamat datang di profil Anda",
			"user":    userData,
		})
	})

	// Route 3: Logout
	e.POST("/logout", func(c echo.Context) error {
		sessionID := c.Request().Header.Get("X-Session-ID")
		if sessionID != "" {
			sessionStore.DestroySession(c.Request().Context(), sessionID)
		}
		return c.JSON(http.StatusOK, map[string]string{"message": "Logout berhasil"})
	})

	log.Println("Server Session berjalan di port :8080")
	if err := e.Start(":8080"); err != nil {
		log.Fatalf("Server berhenti: %v", err)
	}
}
