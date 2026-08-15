package middleware

import (
	"fmt"

	"github.com/labstack/echo/v5"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/codes"
	"go.opentelemetry.io/otel/propagation"
	semconv "go.opentelemetry.io/otel/semconv/v1.26.0"
	"go.opentelemetry.io/otel/trace"
)

// OtelTracing returns an Echo middleware that creates a span for each HTTP request.
func OtelTracing(serviceName string) echo.MiddlewareFunc {
	tracer := otel.Tracer(serviceName)

	return func(next echo.HandlerFunc) echo.HandlerFunc {
		return func(c *echo.Context) error {
			req := c.Request()
			ctx := req.Context()

			// Extract trace context from incoming request headers.
			ctx = otel.GetTextMapPropagator().Extract(ctx, propagation.HeaderCarrier(req.Header))

			// Create a new span for this request.
			spanName := fmt.Sprintf("%s %s", req.Method, c.Path())
			ctx, span := tracer.Start(ctx, spanName,
				trace.WithSpanKind(trace.SpanKindServer),
				trace.WithAttributes(
					semconv.HTTPRequestMethodKey.String(req.Method),
					semconv.URLPath(req.URL.Path),
					semconv.ServerAddress(req.Host),
					semconv.UserAgentOriginal(req.UserAgent()),
				),
			)
			defer span.End()

			// Inject the traced context back into the request.
			c.SetRequest(req.WithContext(ctx))

			// Process the request.
			err := next(c)

			// Record the response status via type assertion to *echo.Response.
			if resp, ok := c.Response().(*echo.Response); ok {
				status := resp.Status
				span.SetAttributes(attribute.Int("http.response.status_code", status))

				if status >= 400 {
					span.SetStatus(codes.Error, fmt.Sprintf("HTTP %d", status))
				} else {
					span.SetStatus(codes.Ok, "")
				}
			}

			if err != nil {
				span.RecordError(err)
				span.SetStatus(codes.Error, err.Error())
			}

			return err
		}
	}
}
