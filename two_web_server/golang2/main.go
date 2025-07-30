package main

import (
	"context"
	"encoding/json"
	"errors"
	"net/http"
	"os"
	"os/signal"
	"time"

	commondmiddlewares "golang2-note-two-web-server/commons/middlewares"
	httproutercontroller "golang2-note-two-web-server/controllers"
	echoroutes "golang2-note-two-web-server/features/echo_landing_page/landing_page/routes"
	httprouterroutes "golang2-note-two-web-server/routes"

	"github.com/julienschmidt/httprouter"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func notFoundHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusNotFound)

	json.NewEncoder(w).Encode(map[string]interface{}{
		"error":   "Not Found",
		"message": "The requested route does not exist httprouter",
	})
}

func methodNotAllowedHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusMethodNotAllowed)

	json.NewEncoder(w).Encode(map[string]interface{}{
		"error":   "Method Not Allowed",
		"message": "The method is not allowed for the requested URL httprouter",
	})
}

func CustomHTTPErrorHandler(err error, c echo.Context) {
	he, ok := err.(*echo.HTTPError)
	if !ok {
		err = errors.New("cannot convert error to echo.HTTPError")
		c.JSON(http.StatusInternalServerError, map[string]string{
			"resposne": "internal server error echoi",
		})
		return
	}

	var message string
	if he.Code == http.StatusNotFound {
		message = "not found echo"
	} else if he.Code == http.StatusMethodNotAllowed {
		message = "method not allowed echo"
	} else {
		message = "internal server error echo"
	}
	c.JSON(he.Code, map[string]string{
		"response": message,
	})
}

func main() {
	e := echo.New()
	e.Use(middleware.Recover())
	e.Use(commondmiddlewares.EchoGlobalExampleMiddleware)
	e.HTTPErrorHandler = CustomHTTPErrorHandler
	echoroutes.SetRoute(e)

	router := httprouter.New()
	router.HandleMethodNotAllowed = true
	router.MethodNotAllowed = http.HandlerFunc(methodNotAllowedHandler)
	router.NotFound = http.HandlerFunc(notFoundHandler)
	httprouterController := httproutercontroller.NewHttprouterController()
	httprouterroutes.SetHttprouterRoute(router, httprouterController)

	e.Any("/*", echo.WrapHandler(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		router.ServeHTTP(w, r)
	})))

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
