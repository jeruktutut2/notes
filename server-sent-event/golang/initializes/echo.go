package initializes

import (
	"fmt"
	"net/http"
	"server_sent_event/middlewares"

	"github.com/labstack/echo/v4"
)

func CustomHTTPErrorHandler(err error, c echo.Context) {
	requestId := c.Request().Context().Value(middlewares.RequestIdKey).(string)
	fmt.Println("requestId:", requestId)
	he, ok := err.(*echo.HTTPError)
	if !ok {
		c.JSON(http.StatusInternalServerError, map[string]interface{}{
			"response": "cannot convert error to echo.HTTPError",
		})
		return
	}

	var message string
	if he.Code == http.StatusNotFound {
		message = "not found"
	} else if he.Code == http.StatusMethodNotAllowed {
		message = "method not allowed"
	} else {
		message = "internal server error"
	}
	c.JSON(he.Code, map[string]interface{}{
		"response": message,
	})
}
