FROM golang:alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o app_main main.go

FROM alpine:latest
RUN apk add --no-cache curl jq
WORKDIR /app
COPY --from=builder /app/app_main .

EXPOSE 8080
CMD ["./app_main"]
