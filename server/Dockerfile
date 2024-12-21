FROM golang:1.21-alpine

WORKDIR /app

# Install git for private repo access
RUN apk add --no-cache git

# Copy go mod files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy source code
COPY . .

COPY data/galaxy_data.json ./data/galaxy_data.json

# Build the application
RUN go build -o main ./cmd/server/main.go

# Expose the port the server runs on
EXPOSE 8080

# Run the server
CMD ["./main"] 