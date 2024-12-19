package handlers

import (
	"github.com/Polkadoty/Space-Farce/internal/game"
	"github.com/gorilla/websocket"
)

func handleWebSocket(conn *websocket.Conn, games *game.Manager) {
	// Get query parameters from the original request
	query := conn.LocalAddr().String() // Temporary, just to compile
	gameID := query
	playerID := query

	game, exists := games.GetGame(gameID)
	if !exists {
		conn.Close()
		return
	}

	// Create a new player if they don't exist
	player, exists := game.Players[playerID]
	if !exists {
		player = game.NewPlayer(playerID, "Player"+playerID[:8])
		if err := game.AddPlayer(player); err != nil {
			conn.Close()
			return
		}
	}

	connection := game.NewConnection(player, conn)
	game.RegisterConnection(player, connection)

	go connection.WritePump()
	connection.ReadPump()
}
