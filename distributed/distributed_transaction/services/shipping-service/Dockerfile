FROM golang:1.22-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /shipping-service ./services/shipping-service/cmd/main.go

FROM alpine:3.19
RUN apk --no-cache add ca-certificates
COPY --from=builder /shipping-service /shipping-service
EXPOSE 8084
CMD ["/shipping-service"]
