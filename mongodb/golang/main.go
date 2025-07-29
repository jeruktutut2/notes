package main

import (
	"context"
	"net/http"
	"note-golang-mongodb/helpers"
	"note-golang-mongodb/routes"
	"note-golang-mongodb/utils"
	"os"
	"os/signal"
	"time"

	"github.com/labstack/echo/v4"
)

func main() {
	mongoUtil := utils.NewMongoDbConnection("localhost", "root", "12345", "test1", "27017", 10, 3, 900)
	defer mongoUtil.Close("localhost", "27127")
	uuidHelper := helpers.NewUuidHelper()
	e := echo.New()
	routes.SetRoute(e, mongoUtil, uuidHelper)

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
