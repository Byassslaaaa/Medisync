# Stage 1: Build
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy go.mod dan download dependencies
COPY go.mod go.sum* ./
RUN go mod download

# Copy semua source code
COPY . .

# Build binary
RUN CGO_ENABLED=0 GOOS=linux go build -o service-a ./cmd/main.go

# Stage 2: Run (image minimal)
FROM alpine:3.19

WORKDIR /app

COPY --from=builder /app/service-a .

EXPOSE 4001

CMD ["./service-a"]
