package main

import (
	"context"
	"net/http"
	"note-golang-postgresql/controllers"
	"note-golang-postgresql/repositories"
	"note-golang-postgresql/routes"
	"note-golang-postgresql/services"
	"note-golang-postgresql/utils"
	"os"
	"os/signal"
	"time"

	"github.com/labstack/echo/v4"
)

func main() {
	postgresUtil := utils.NewPostgresUtil("localhost", "postgres", "12345", "test1", "5432", "test1", 10, 10, 10, 10)
	// fmt.Println("postgresUtil:", postgresUtil)
	e := echo.New()
	postgresRepository := repositories.NewPostgresRepository()
	postgresService := services.NewPostgresService(postgresUtil, postgresRepository)
	postgresController := controllers.NewPostgresController(postgresService)
	routes.SetRoute(e, postgresController)

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
