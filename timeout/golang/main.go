package main

import (
	"context"
	"net/http"
	"os"
	"os/signal"
	"time"
	"timeout/controllers"
	"timeout/repositories"
	"timeout/routes"
	"timeout/services"
	"timeout/utils"

	"github.com/labstack/echo/v4"
	"github.com/labstack/gommon/log"
)

func main() {
	postgresUtil := utils.NewPostgresUtil()
	defer postgresUtil.Close()

	e := echo.New()
	e.Logger.SetLevel(log.INFO)

	test1Repository := repositories.NewTest1Repository()
	test2Repository := repositories.NewTest2Repository()
	test3Repository := repositories.NewTest3Repository()
	testService := services.NewTestService(postgresUtil, test1Repository, test2Repository, test3Repository)
	testController := controllers.NewTestController(testService)
	routes.TestRoute(e, testController)

	e.GET("/", func(c echo.Context) error {
		time.Sleep(5 * time.Second)
		return c.JSON(http.StatusOK, "OK")
	})

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
