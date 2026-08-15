FROM golang:1.22-alpine AS builder

WORKDIR /app
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o flash_sale_service main.go

FROM alpine:latest
WORKDIR /root/
COPY --from=builder /app/flash_sale_service .
COPY deduct_stock.lua .
EXPOSE 8082
CMD ["./flash_sale_service"]
