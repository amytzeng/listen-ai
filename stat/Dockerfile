# stat/Dockerfile
# Build a small Go image for the stat service using multi-stage build.

FROM golang:1.24-alpine AS builder

# Ensure CA certificates exist for any HTTPS fetches during module download.
RUN apk add --no-cache ca-certificates

WORKDIR /src

# Download modules first to leverage Docker cache.
COPY go.mod go.sum /src/
RUN go mod download

# Copy the remaining source and build.
COPY . /src
RUN CGO_ENABLED=0 GOOS=linux go build -o /out/stat .

# Final runtime image.
FROM alpine:3.20

RUN apk add --no-cache ca-certificates

WORKDIR /app

# Copy the compiled binary.
COPY --from=builder /out/stat /app/stat

# Default port and SQLite path are configurable via env.
EXPOSE 8002
ENV STAT_PORT=8002 \
    SQLITE_PATH=/data/listenai.db

# Run the service.
CMD ["/app/stat"]