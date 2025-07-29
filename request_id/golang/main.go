package main

import (
	"net/http"
	"request_id/middlewares"

	"github.com/labstack/echo/v4"
)

func main() {
	e := echo.New()
	e.GET("/request-id", func(c echo.Context) error {
		requestId, ok := c.Request().Context().Value(middlewares.RequestIdKey).(string)
		if !ok {
			return c.String(http.StatusOK, "requestId")
		}
		return c.JSON(http.StatusOK, map[string]interface{}{
			"data": map[string]interface{}{
				"requestId": requestId,
			},
			"errors": nil,
		})
	}, middlewares.SetRequestId)
	e.Logger.Fatal(e.Start(":8080"))
}
