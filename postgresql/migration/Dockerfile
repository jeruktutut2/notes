# ==========================================
# DOCKERFILE - Multi-stage Build
# ==========================================
# Stage 1: Build Go binary
# Stage 2: Minimal runtime image
# ==========================================

# ---- Stage 1: Builder ----
FROM golang:1.25-alpine AS builder

# Install dependencies yang diperlukan
RUN apk add --no-cache git ca-certificates tzdata

# Set working directory
WORKDIR /app

# Copy go.mod dan go.sum terlebih dahulu (untuk Docker layer caching)
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy seluruh source code
COPY . .

# Build binary
# CGO_ENABLED=0 = static binary (tidak perlu libc)
# -ldflags="-s -w" = strip debug info (binary lebih kecil)
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-s -w" -o /app/server ./cmd/api

# ---- Stage 2: Runtime ----
FROM alpine:3.21

# Install ca-certificates dan timezone data
RUN apk add --no-cache ca-certificates tzdata

# Set timezone
ENV TZ=Asia/Jakarta

# Buat user non-root untuk keamanan
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set working directory
WORKDIR /app

# Copy binary dari builder stage
COPY --from=builder /app/server .

# Copy migration files (untuk CLI usage juga)
COPY --from=builder /app/migrations/sql ./migrations/sql

# Ganti ke user non-root
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -qO- http://localhost:8080/health || exit 1

# Jalankan server
ENTRYPOINT ["./server"]
