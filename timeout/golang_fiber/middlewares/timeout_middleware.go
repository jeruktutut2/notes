package middlewares

import (
	"context"
	"errors"
	"fmt"
	"log"
	"time"

	"github.com/gofiber/fiber/v2"
)

func TimeoutMiddleware(timeout time.Duration) fiber.Handler {
	return func(c *fiber.Ctx) error {
		// Buat context dengan timeout
		ctx, cancel := context.WithTimeout(c.Context(), timeout)
		defer cancel()

		// Ganti context lama dengan context yang memiliki timeout
		c.SetUserContext(ctx)

		// Jalankan handler berikutnya
		errCh := make(chan error, 1)

		go func() {
			fmt.Println("kesini", 1)
			errCh <- c.Next()
			fmt.Println("kesini", 2)
		}()

		// select {
		// case <-ctx.Done():
		// 	// Jika timeout terjadi
		// 	log.Println("Request timeout:", c.OriginalURL())
		// 	return fiber.NewError(fiber.StatusRequestTimeout, "Request timeout")
		// case err := <-errCh:
		// 	// Handler selesai sebelum timeout
		// 	log.Println("Handler selesai sebelum timeout")
		// 	return err
		// }
		select {
		case <-ctx.Done():
			// Context selesai karena timeout atau client menutup koneksi
			if errors.Is(ctx.Err(), context.DeadlineExceeded) {
				log.Println("Timeout: request took too long:", c.OriginalURL())
				return fiber.NewError(fiber.StatusRequestTimeout, "Request timeout")
			}
			if errors.Is(ctx.Err(), context.Canceled) {
				log.Println("Client closed connection early:", c.OriginalURL())
				return fiber.NewError(fiber.StatusRequestTimeout, "Client closed request")
			}
			// Fallback: error context lainnya
			return fiber.ErrInternalServerError

		case err := <-errCh:
			// Handler selesai lebih dulu
			return err
		}
	}
}
