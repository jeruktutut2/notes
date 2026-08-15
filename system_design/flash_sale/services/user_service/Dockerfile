FROM golang:1.22-alpine AS builder

WORKDIR /app
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o user_service main.go

FROM alpine:latest
WORKDIR /root/
COPY --from=builder /app/user_service .
EXPOSE 8081
CMD ["./user_service"]
