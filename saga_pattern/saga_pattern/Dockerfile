# Build stage
FROM golang:1.22-alpine AS builder

RUN apk add --no-cache ca-certificates tzdata

WORKDIR /app

# Dependency layer caching
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# ARG to specify which service to build (default: kafka_saga)
ARG SERVICE_NAME=kafka_saga

# Build lightweight static binary
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/main ./cmd/${SERVICE_NAME}

# Runtime stage
FROM alpine:3.19

RUN apk add --no-cache ca-certificates tzdata

WORKDIR /app

COPY --from=builder /app/main .

CMD ["./main"]
