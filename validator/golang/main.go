package main

import (
	"context"
	"net/http"
	"note-validator-golang/helpers"
	"note-validator-golang/initialize"
	"note-validator-golang/models/requests"
	"os"
	"os/signal"
	"time"

	"github.com/go-playground/validator/v10"
	"github.com/labstack/echo/v4"
)

func main() {
	e := echo.New()
	validate := validator.New()
	initialize.UsernameValidator(validate)
	initialize.PasswordValidator(validate)
	initialize.TelephoneValidator(validate)
	e.POST("/test", func(c echo.Context) error {
		var testValidatorRequest requests.TestValidatorRequest
		err := c.Bind(&testValidatorRequest)
		if err != nil {
			return c.JSON(http.StatusBadRequest, map[string]interface{}{
				"response": err.Error(),
			})
		}
		err = validate.Struct(testValidatorRequest)
		if err != nil {
			httpResponse := helpers.GetValidatorError(err, testValidatorRequest)
			return c.JSON(httpResponse.HttpStatusCode, httpResponse.Response)
		}

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
