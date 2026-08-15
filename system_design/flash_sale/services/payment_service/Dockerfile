FROM golang:1.22-alpine AS builder

WORKDIR /app
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o payment_service main.go

FROM alpine:latest
WORKDIR /root/
COPY --from=builder /app/payment_service .
COPY restore_stock.lua .
EXPOSE 8084
CMD ["./payment_service"]
