package main

import (
	"context"
	"net/http"
	"note-golang-redis/controllers"
	"note-golang-redis/routes"
	"note-golang-redis/services"
	"note-golang-redis/utils"
	"os"
	"os/signal"
	"time"

	"github.com/labstack/echo/v4"
)

func main() {
	residUtil := utils.NewRedisUtil("localhost", "6380", 0)
	redisService := services.NewRedisService(residUtil)
	redisController := controllers.NewRedisController(redisService)
	e := echo.New()
	routes.SetRedisRoute(e, redisController)
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()
	go func() {
		if err := e.Start(":8080"); err != nil && err != http.ErrServerClosed {
			e.Logger.Fatal("shutting down the server")
		}
	}()

	<-ctx.Done()
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := e.Shutdown(ctx); err != nil {
		e.Logger.Fatal(err)
	}
}
