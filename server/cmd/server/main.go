package main

import (
	"log"

	"github.com/Polkadoty/Space-Farce/internal/config"
	"github.com/Polkadoty/Space-Farce/internal/server"
)

func main() {
	cfg := config.Load()

	srv, err := server.New(cfg)
	if err != nil {
		log.Fatalf("Failed to create server: %v", err)
	}

	if err := srv.Run(); err != nil {
		log.Fatalf("Server error: %v", err)
	}
}
