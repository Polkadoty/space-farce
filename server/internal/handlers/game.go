package handlers

import (
	"net/http"

	"github.com/Polkadoty/Space-Farce/internal/game"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/gorilla/websocket"
)

type CreateGameRequest struct {
	Scenario   string `json:"scenario"`
	MaxPlayers int    `json:"max_players"`
	GalaxySize int    `json:"galaxy_size"`
	Seed       int64  `json:"seed"`
}

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		// TODO: Implement proper origin checking
		return true
	},
}

func CreateGame(games *game.Manager) gin.HandlerFunc {
	return func(c *gin.Context) {
		var req CreateGameRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request"})
			return
		}

		game, err := games.CreateGame(req.Seed, req.MaxPlayers, req.GalaxySize)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		c.JSON(http.StatusOK, game)
	}
}

func ListGames(games *game.Manager) gin.HandlerFunc {
	return func(c *gin.Context) {
		c.JSON(http.StatusOK, games.ListGames())
	}
}

func GetGame(games *game.Manager) gin.HandlerFunc {
	return func(c *gin.Context) {
		id := c.Param("id")
		game, exists := games.GetGame(id)
		if !exists {
			c.JSON(http.StatusNotFound, gin.H{"error": "Game not found"})
			return
		}
		c.JSON(http.StatusOK, game)
	}
}

func GameWebSocket(games *game.Manager) gin.HandlerFunc {
	return func(c *gin.Context) {
		conn, err := upgrader.Upgrade(c.Writer, c.Request, nil)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "WebSocket upgrade failed"})
			return
		}

		// TODO: Implement WebSocket handler
		go handleWebSocket(conn, games)
	}
}

func JoinGame(games *game.Manager) gin.HandlerFunc {
	return func(c *gin.Context) {
		id := c.Param("id")
		game, exists := games.GetGame(id)
		if !exists {
			c.JSON(http.StatusNotFound, gin.H{"error": "Game not found"})
			return
		}

		// Create a new player
		playerID := uuid.New().String()
		player := game.NewPlayer(playerID, "Player"+playerID[:8])

		if err := game.AddPlayer(player); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		c.JSON(http.StatusOK, player)
	}
}
