package main

import (
	"context"
	"golang-note-mqtt/consumers"
	"golang-note-mqtt/routes"
	"golang-note-mqtt/utils"
	"net/http"
	"os"
	"os/signal"
	"time"

	"github.com/labstack/echo/v4"
)

func main() {
	mqttUtil := utils.NewMqttUtil()
	defer mqttUtil.Close()
	consumers.NewMqttConsumer(mqttUtil.GetClient())

	e := echo.New()
	routes.SetMqttRoute(e, mqttUtil.GetClient())
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
