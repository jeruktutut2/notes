package controllers

import (
	"golang-note-open-telemetry/services"
	"net/http"

	"github.com/labstack/echo/v4"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
)

type OtelController interface {
	SetSpan(c echo.Context) error
}

type otelController struct {
	otelService services.OtelService
}

func NewOtelController(otelService services.OtelService) OtelController {
	return &otelController{
		otelService: otelService,
	}
}

func (controller *otelController) SetSpan(c echo.Context) error {
	ctx, span := otel.Tracer("echo-server").Start(c.Request().Context(), "set-span")
	defer span.End()
	// fmt.Println("ctx:", ctx)

	span.SetAttributes(attribute.String("span.attribute", "thisisatribute"))

	_, subSpan := otel.Tracer("echo-server").Start(ctx, "otelService")
	result := controller.otelService.SetSpan(ctx)
	subSpan.End()

	return c.JSON(http.StatusOK, map[string]string{
		"response": result,
	})
}
