package handlers

import (
	modelrequests "golang-rsa/models/requests"
	"golang-rsa/services"
	"net/http"

	"github.com/labstack/echo/v4"
)

type KeyHandler interface {
	Sign(c echo.Context) error
	Verify(c echo.Context) error
}

type keyHandler struct {
	keyService services.KeyService
}

func NewKeyHandler(keyService services.KeyService) KeyHandler {
	return &keyHandler{
		keyService: keyService,
	}
}

func (handler *keyHandler) Sign(c echo.Context) error {
	var signRequest modelrequests.SignRequest
	err := c.Bind(&signRequest)
	if err != nil {
		return c.JSON(http.StatusBadRequest, echo.Map{
			"response": err.Error(),
		})
	}
	httpStatusCode, response := handler.keyService.Sign(c.Request().Context(), signRequest)
	return c.JSON(httpStatusCode, response)
}

func (handler *keyHandler) Verify(c echo.Context) error {
	var verifyRequest modelrequests.VerifyRequest
	err := c.Bind(&verifyRequest)
	if err != nil {
		return c.JSON(http.StatusBadRequest, echo.Map{
			"response": err.Error(),
		})
	}
	httpStatusCode, response := handler.keyService.Verify(c.Request().Context(), verifyRequest)
	return c.JSON(httpStatusCode, response)
}
