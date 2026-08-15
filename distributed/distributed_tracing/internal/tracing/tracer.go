package tracing

import (
	"context"
	"log"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.17.0"
)

// InitTracer melakukan inisialisasi OpenTelemetry (OTel)
// dan mengarahkan data trace ke Jaeger via OTLP HTTP.
func InitTracer(serviceName, jaegerEndpoint string) (*sdktrace.TracerProvider, error) {
	ctx := context.Background()

	// 1. Buat Exporter untuk mengirim data ke Jaeger
	exporter, err := otlptracehttp.New(ctx,
		otlptracehttp.WithEndpoint(jaegerEndpoint),
		otlptracehttp.WithInsecure(), // tanpa HTTPS untuk contoh lokal
	)
	if err != nil {
		return nil, err
	}

	// 2. Tentukan identitas service ini (muncul di UI Jaeger)
	res, err := resource.New(ctx,
		resource.WithAttributes(
			semconv.ServiceName(serviceName),
		),
	)
	if err != nil {
		return nil, err
	}

	// 3. Setup Tracer Provider dengan sampling 100% (semua request direkam)
	tp := sdktrace.NewTracerProvider(
		sdktrace.WithBatcher(exporter),
		sdktrace.WithResource(res),
		sdktrace.WithSampler(sdktrace.AlwaysSample()),
	)

	// Set provider ini sebagai global standard
	otel.SetTracerProvider(tp)

	// 4. Setup Propagator agar TraceID bisa menular (propagate)
	// melalui HTTP Headers (W3C Trace Context) saat service A memanggil service B
	otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(
		propagation.TraceContext{},
		propagation.Baggage{},
	))

	log.Printf("✅ Tracer %s berhasil diinisialisasi (Target: %s)", serviceName, jaegerEndpoint)
	return tp, nil
}
