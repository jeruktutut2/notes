package main

import (
	"context"
	"fmt"
	"log"
	"note-golang-fiber-timeout/routes"
	"note-golang-fiber-timeout/utils"
	"os"
	"os/signal"
	"time"

	"github.com/gofiber/fiber/v2"
)

func main() {
	postgresUtil := utils.NewPostgresUtil()
	defer postgresUtil.Close()

	app := fiber.New(fiber.Config{
		IdleTimeout:  time.Second * 60,
		WriteTimeout: time.Second * 60,
		ReadTimeout:  time.Second * 60,
		Prefork:      true,
	})
	// app.Use(middlewares.TimeoutMiddleware(time.Duration(7) * time.Second))
	routes.SetRoute(app, postgresUtil)
	go func() {
		if err := app.Listen(":8080"); err != nil {
			log.Panic(err)
		}
	}()

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()
	<-ctx.Done()
	fmt.Println("Gracefully shutting down...")
	_ = app.Shutdown()
	fmt.Println("Running cleanup tasks...")
	fmt.Println("Fiber was successful shutdown.")
}
