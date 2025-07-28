package main

import (
	"context"
	"net/http"
	"note-golang-memcached/routes"
	"note-golang-memcached/utils"
	"os"
	"os/signal"
	"time"

	"github.com/labstack/echo/v4"
)

func main() {
	memcachedUtil := utils.NewMemcachedUtil()
	defer memcachedUtil.Close()

	e := echo.New()
	routes.SetMemcachedRoute(e, memcachedUtil)

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
