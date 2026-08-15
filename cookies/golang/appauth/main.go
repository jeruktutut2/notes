package main

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func main() {
	e := echo.New()
	e.GET("/", func(c echo.Context) error {
		c.SetCookie(&http.Cookie{
			Name:     "session",
			Value:    "cookieappa",
			Domain:   "appa.local",
			Path:     "/",
			HttpOnly: true,
			Secure:   true,
		})

		c.SetCookie(&http.Cookie{
			Name:     "session",
			Value:    "cookieappb",
			Domain:   "appb.local",
			Path:     "/",
			HttpOnly: true,
			Secure:   true,
		})
		return c.String(200, "Hello, World appauth")
	})
	e.Start("appauth.local:8080")
}
