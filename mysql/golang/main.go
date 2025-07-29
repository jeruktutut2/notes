package main

import (
	"context"
	"log"
	"net/http"
	"note-golang-mysql/controllers"
	"note-golang-mysql/repositories"
	"note-golang-mysql/routes"
	"note-golang-mysql/services"
	"note-golang-mysql/utils"
	"os"
	"os/signal"
	"time"

	"github.com/labstack/echo/v4"
)

func main() {
	mysqlUtil := utils.NewMysqlUtil("localhost", "root", "12345", "test1", "3309", 10, 10, 10, 10)
	defer mysqlUtil.Close("localhost", "3309")

	e := echo.New()
	mysqlRepository := repositories.NewMysqlRepository()
	mysqlService := services.NewMysqlService(mysqlUtil, mysqlRepository)
	mysqlController := controllers.NewMysqlController(mysqlService)
	routes.SetRoute(e, mysqlController)

	go func() {
		if err := e.Start("localhost:8080"); err != nil && err != http.ErrServerClosed {
			log.Fatalln("shutting down the server:", err)
		}
	}()

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()

	<-ctx.Done()
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := e.Shutdown(ctx); err != nil {
		e.Logger.Fatal(err)
	}

}
