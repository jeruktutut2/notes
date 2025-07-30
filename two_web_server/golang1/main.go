package main

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	httproutercontroller "golang-note-two-web-server/controllers"
	echoroutes "golang-note-two-web-server/features/echo_landing_page/landing_page/routes"
	httprouterroutes "golang-note-two-web-server/routes"
	"log"
	"net/http"
	"net/http/httptest"
	"os"
	"os/signal"
	"time"

	"github.com/julienschmidt/httprouter"
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

type MultiMux struct {
	echo       *echo.Echo
	httpRouter *httprouter.Router
}

func (m *MultiMux) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	rec := httptest.NewRecorder()
	m.echo.ServeHTTP(rec, r)

	fmt.Println("echo rec.Code:", rec.Code)
	if rec.Code == http.StatusNotFound {
		m.httpRouter.ServeHTTP(w, r)
		return
	}

	for k, vv := range rec.Result().Header {
		for _, v := range vv {
			w.Header().Add(k, v)
		}
	}
	w.WriteHeader(rec.Code)
	_, _ = w.Write(rec.Body.Bytes())
}

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
	e.HTTPErrorHandler = CustomHTTPErrorHandler
	echoroutes.SetRoute(e)

	router := httprouter.New()
	router.HandleMethodNotAllowed = true
	router.MethodNotAllowed = http.HandlerFunc(methodNotAllowedHandler)
	router.NotFound = http.HandlerFunc(notFoundHandler)
	httprouterController := httproutercontroller.NewHttprouterController()
	httprouterroutes.SetHttprouterRoute(router, httprouterController)

	multiMux := &MultiMux{
		echo:       e,
		httpRouter: router,
	}

	server := &http.Server{
		Addr:    ":8080",
		Handler: multiMux,
	}

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()

	go func() {
		log.Println("Server running at http://localhost:8080")
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Server error: %v", err)
		}
	}()

	<-ctx.Done()
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := e.Shutdown(ctx); err != nil {
		e.Logger.Fatal(err)
	}
	if err := server.Shutdown(ctx); err != nil {
		log.Fatalf("Server shutdown error: %v", err)
	}
	log.Println("Server gracefully stopped")
}
