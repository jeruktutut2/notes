FROM golang:1.22-alpine AS builder

WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build the service
RUN CGO_ENABLED=0 GOOS=linux go build -o /order-service ./services/order-service/cmd/main.go

# Final stage
FROM alpine:3.19

RUN apk --no-cache add ca-certificates

COPY --from=builder /order-service /order-service

EXPOSE 8081

CMD ["/order-service"]
