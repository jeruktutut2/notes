package main

import (
	"context"
	"net/http"
	"note-golang-cockroachdb/routes"
	"note-golang-cockroachdb/utils"
	"os"
	"os/signal"
	"time"

	"github.com/labstack/echo/v4"
)

func main() {
	cockroachDbUtil := utils.NewCockroachDbutil()

	e := echo.New()
	routes.SetRoute(e, cockroachDbUtil)

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
