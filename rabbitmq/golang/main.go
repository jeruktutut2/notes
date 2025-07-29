package main

import (
	"context"
	"net/http"
	"note-golang-rabbitmq/consumers"
	"note-golang-rabbitmq/routes"
	"note-golang-rabbitmq/utils"
	"os"
	"os/signal"
	"time"

	"github.com/labstack/echo/v4"
)

func main() {
	rabbitmqUtil := utils.NewRabbitmqConnection("localhost", "user", "password", "5672")
	defer rabbitmqUtil.Close("localhost", "5672")

	rabbitmqConsumer := consumers.NewRabbitmqConsumer(rabbitmqUtil.GetChannel())
	rabbitmqConsumer.ReadTextMessage()

	e := echo.New()
	routes.SetRabbitmqRoute(e, rabbitmqUtil.GetChannel())

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
