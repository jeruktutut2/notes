# ============================================
# Dockerfile - Golang Echo v5 Application
# Multi-stage build for minimal image size
# ============================================

# Stage 1: Build the Go application
FROM golang:1.25-alpine AS builder

RUN apk add --no-cache git ca-certificates tzdata

WORKDIR /app

# Copy all source code
COPY app/ .

# Download dependencies and build
RUN go mod tidy && \
    CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-w -s -X main.version=1.0.0" -o /drc-app .

# Stage 2: Minimal runtime image
FROM alpine:3.20

RUN apk add --no-cache \
    ca-certificates \
    tzdata \
    curl \
    postgresql16-client

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copy binary from builder
COPY --from=builder /drc-app .

# Set ownership
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8080

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

ENTRYPOINT ["./drc-app"]
