package initialize

import (
	"errors"
	"net/http"
	"note-golang-panic/helpers"

	"github.com/labstack/echo/v4"
)

func CustomHTTPErrorHandler(err error, c echo.Context) {
	requestId := "requestId"
	helpers.PrintLogToTerminal(err, requestId)
	he, ok := err.(*echo.HTTPError)
	if !ok {
		err = errors.New("cannot convert error to echo.HTTPError")
		helpers.PrintLogToTerminal(err, requestId)
		c.JSON(http.StatusInternalServerError, map[string]string{
			"response": "internal server error",
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
	c.JSON(he.Code, map[string]string{
		"response": message,
	})
}
