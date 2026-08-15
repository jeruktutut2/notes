# Build stage
FROM golang:1.25-alpine AS builder

WORKDIR /app

COPY . .
RUN go mod tidy
RUN go mod download

RUN CGO_ENABLED=0 GOOS=linux go build -o server main.go

# Production stage
FROM alpine:3.19

WORKDIR /app

COPY --from=builder /app/server /app/server

EXPOSE 8080

CMD ["/app/server"]
