# Stage 1: Build
FROM golang:1.21-alpine AS builder

WORKDIR /app

COPY go.mod go.sum* ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o service-b ./cmd/main.go

# Stage 2: Run
FROM alpine:3.19

WORKDIR /app

COPY --from=builder /app/service-b .

EXPOSE 4002 50052

CMD ["./service-b"]
