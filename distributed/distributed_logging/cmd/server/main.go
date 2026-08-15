package main

import (
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/labstack/echo/v4"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

func main() {
	// 1. Setup Log Directory
	os.MkdirAll("logs", 0755)
	
	// Buka file log
	logFile, err := os.OpenFile("logs/app.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		panic(err)
	}
	defer logFile.Close()

	// 2. Konfigurasi Zap Logger untuk output JSON terstruktur
	encoderConfig := zap.NewProductionEncoderConfig()
	encoderConfig.TimeKey = "timestamp"
	encoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder

	// Kita tulis log ke File (diambil oleh Promtail) DAN ke Console (untuk dilihat langsung)
	core := zapcore.NewTee(
		zapcore.NewCore(zapcore.NewJSONEncoder(encoderConfig), zapcore.AddSync(logFile), zap.InfoLevel),
		zapcore.NewCore(zapcore.NewConsoleEncoder(encoderConfig), zapcore.AddSync(os.Stdout), zap.InfoLevel),
	)

	logger := zap.New(core)
	defer logger.Sync()

	e := echo.New()
	
	// ID Service unik
	serviceID := os.Getenv("SERVICE_ID")
	if serviceID == "" {
		serviceID = "Auth-Service"
	}

	// Middleware Logging yang menyuntikkan (inject) konteks
	e.Use(func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c echo.Context) error {
			start := time.Now()
			
			// Dummy Trace ID
			traceID := fmt.Sprintf("trace-%d", time.Now().UnixNano())
			
			// Tambahkan fields (konteks terstruktur) ke log
			reqLogger := logger.With(
				zap.String("service", serviceID),
				zap.String("trace_id", traceID),
				zap.String("method", c.Request().Method),
				zap.String("path", c.Request().URL.Path),
			)

			// Simpan logger di context agar bisa dipakai di handler
			c.Set("logger", reqLogger)

			reqLogger.Info("Request dimulai")
			
			err := next(c)
			
			reqLogger.Info("Request selesai", 
				zap.Duration("latency", time.Since(start)),
				zap.Int("status", c.Response().Status),
			)
			
			return err
		}
	})

	e.GET("/login", func(c echo.Context) error {
		logr := c.Get("logger").(*zap.Logger)
		
		logr.Info("User mencoba login", zap.String("username", "johndoe"))
		
		// Simulasi error
		logr.Error("Gagal terhubung ke database otentikasi", zap.String("db_host", "10.0.0.5"))
		
		return c.JSON(http.StatusInternalServerError, map[string]string{
			"error": "Internal Server Error",
		})
	})

	logger.Info("🚀 Server berjalan di port 8080", zap.String("service", serviceID))
	e.Start(":8080")
}
